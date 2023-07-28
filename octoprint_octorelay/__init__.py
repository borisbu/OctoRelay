# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
from octoprint.events import Events
from octoprint.util import ResettableTimer
from octoprint.util import RepeatedTimer
from octoprint.access.permissions import Permissions

from octoprint_octorelay.const import DEFAULT_SETTINGS, RELAY_INDEXES, TEMPLATES, ASSETS
from octoprint_octorelay.const import SWITCH_PERMISSION, UPDATES_CONFIG, POLLING_INTERVAL
from octoprint_octorelay.const import UPDATE_COMMAND, GET_STATUS_COMMAND, LIST_ALL_COMMAND, AT_COMMAND

import flask
import RPi.GPIO as GPIO
import os

class OctoRelayPlugin(
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.ShutdownPlugin,
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.RestartNeedingPlugin
):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.polling_timer = None
        self.turn_off_timers = {}
        self.model = {}
        for index in RELAY_INDEXES:
            self.model[index] = {}

    def get_settings_defaults(self):
        return DEFAULT_SETTINGS

    def get_template_configs(self):
        return TEMPLATES

    def get_assets(self):
        return ASSETS

    def on_after_startup(self):
        self._logger.info("--------------------------------------------")
        self._logger.info("start OctoRelay")
        settings = DEFAULT_SETTINGS.copy()

        for index in RELAY_INDEXES:
            settings[index].update(self._settings.get([index]))
            self._logger.debug(f"settings for {index}: {settings[index]}")

            if settings[index]['active']:
                relay_pin = int(settings[index]['relay_pin'])
                initial_value = bool(settings[index]['initial_value'])
                inverted_output = bool(settings[index]['inverted_output'])

                # Setting the default state of pin
                GPIO.setup(relay_pin, GPIO.OUT)
                # XOR with inverted
                GPIO.output(relay_pin, initial_value is not inverted_output)

        self.update_ui()
        self.polling_timer = RepeatedTimer(POLLING_INTERVAL, self.input_polling, daemon=True)
        self.polling_timer.start()

        self._logger.info("OctoRelay plugin started")
        self._logger.info("--------------------------------------------")

    def on_shutdown(self):
        self.polling_timer.cancel()
        self._logger.info("OctoRelay plugin stopped")
        self._logger.info("--------------------------------------------")

    def get_api_commands(self):
        return {
            UPDATE_COMMAND: [ "pin" ],
            GET_STATUS_COMMAND: [ "pin" ],
            LIST_ALL_COMMAND: [],
        }

    def get_additional_permissions(self, *args, **kwargs):
        return [ SWITCH_PERMISSION ]

    def has_switch_permission(self):
        try:
            return Permissions.PLUGIN_OCTORELAY_SWITCH.can() # may raise UnknownPermission(key)
        except Exception:
            return False

    def on_api_command(self, command, data):
        self._logger.debug(f"on_api_command {command}, parameters {data}")

        # API command to get relay statuses
        if command == LIST_ALL_COMMAND:
            GPIO.setwarnings(False)
            activeRelays = []
            for index in RELAY_INDEXES:
                settings = self._settings.get([index], merged=True)
                if settings["active"]:
                    relay_pin = int(settings["relay_pin"])
                    inverted = bool(settings['inverted_output'])
                    GPIO.setup(relay_pin, GPIO.OUT)
                    relayData = {
                        "id": index,
                        "name": settings["labelText"],
                        "active": inverted is not bool(GPIO.input(relay_pin)),
                    }
                    activeRelays.append(relayData)
            return flask.jsonify(activeRelays)

        # API command to get relay status
        if command == GET_STATUS_COMMAND:
            settings = self._settings.get([data["pin"]], merged=True)
            relay_pin = int(settings["relay_pin"])
            inverted = bool(settings['inverted_output'])
            GPIO.setwarnings(False)
            GPIO.setup(relay_pin, GPIO.OUT)
            relayState = inverted is not bool(GPIO.input(relay_pin))
            return flask.jsonify(status=relayState)

        if command == UPDATE_COMMAND:
            if not self.has_switch_permission():
                return flask.abort(403)
            status = self.update_relay(data["pin"])
            return flask.jsonify(status=status)

    def update_relay(self, index):
        try:
            settings = self._settings.get([index], merged=True)

            relay_pin = int(settings["relay_pin"])
            inverted = bool(settings['inverted_output'])
            cmdON = settings['cmdON']
            cmdOFF = settings['cmdOFF']

            GPIO.setwarnings(False)

            GPIO.setup(relay_pin, GPIO.OUT)
            # XOR with inverted
            relayState = inverted is not bool(GPIO.input(relay_pin))

            self._logger.debug(f"OctoRelay before pin: {relay_pin}, inverted: {inverted}, relayState: {relayState}")

            # toggle state
            relayState = not relayState

            GPIO.setup(relay_pin, GPIO.OUT)
            # XOR with inverted
            GPIO.output(relay_pin, inverted is not relayState)

            GPIO.setwarnings(True)
            if relayState:
                if cmdON:
                    self._logger.info(f"OctoRelay system command: {cmdON}")
                    os.system(cmdON)
            else:
                if cmdOFF:
                    self._logger.info(f"OctoRelay system command: {cmdOFF}")
                    os.system(cmdOFF)
            self.update_ui()
            return "ok"
        except Exception as e:
            self._logger.debug(e)
            return "error"

    def on_event(self, event, payload):
        self._logger.debug(f"Got event: {event}")
        if event == Events.CLIENT_OPENED:
            self.update_ui()
        elif event == Events.PRINT_STARTED:
            self.print_started()
        elif event == Events.PRINT_DONE:
            self.print_stopped()
        elif event == Events.PRINT_FAILED:
            self.print_stopped()
        #elif event == Events.PRINT_CANCELLING:
            # self.print_stopped()
        #elif event == Events.PRINT_CANCELLED:
            # self.print_stopped()
        return

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.update_ui()

    def print_started(self):
        for off_timer in self.turn_off_timers:
            try:
                self.turn_off_timers[off_timer].cancel()
                self._logger.info(f"cancelled timer: {off_timer}")
            except Exception:
                self._logger.warn(f"could not cancel timer: {off_timer}")
        for index in RELAY_INDEXES:
            settings = self._settings.get([index], merged=True)

            relay_pin = int(settings["relay_pin"])
            inverted = bool(settings['inverted_output'])
            autoONforPrint = bool(settings['autoONforPrint'])
            cmdON = settings['cmdON']
            active = bool(settings["active"])
            if autoONforPrint and active:
                self._logger.debug(f"turning on pin: {relay_pin}, index: {index}")
                self.turn_on_pin(relay_pin, inverted, cmdON)
        self.update_ui()

    def print_stopped(self):
        for index in RELAY_INDEXES:
            settings = self._settings.get([index], merged=True)

            relay_pin = int(settings["relay_pin"])
            inverted = bool(settings['inverted_output'])
            autoOFFforPrint = bool(settings['autoOFFforPrint'])
            autoOffDelay = int(settings['autoOffDelay'])
            cmdOFF = settings['cmdOFF']
            active = bool(settings["active"])
            if autoOFFforPrint and active:
                self._logger.debug(f"turn off pin: {relay_pin} in {autoOffDelay} seconds. index: {index}")
                self.turn_off_timers[index] = ResettableTimer(
                    autoOffDelay, self.turn_off_pin, [relay_pin, inverted, cmdOFF])
                self.turn_off_timers[index].start()
        self.update_ui()

    def turn_off_pin(self, relay_pin: int, inverted: bool, cmdOFF):
        GPIO.setup(relay_pin, GPIO.OUT)
        # XOR with inverted
        GPIO.output(relay_pin, inverted is not False)
        GPIO.setwarnings(True)
        if cmdOFF:
            os.system(cmdOFF)
        self._logger.info(f"pin: {relay_pin} turned off")
        self.update_ui()

    def turn_on_pin(self, relay_pin: int, inverted: bool, cmdON):
        GPIO.setup(relay_pin, GPIO.OUT)
        # XOR with inverted
        GPIO.output(relay_pin, inverted is False)
        GPIO.setwarnings(True)
        if cmdON:
            os.system(cmdON)
        self._logger.info(f"pin: {relay_pin} turned on")

    def update_ui(self):
        settings = DEFAULT_SETTINGS.copy()
        for index in RELAY_INDEXES:
            settings[index].update(self._settings.get([index]))

            labelText = settings[index]["labelText"]
            active = int(settings[index]["active"]) # todo make it bool later
            relay_pin = int(settings[index]["relay_pin"])
            inverted = bool(settings[index]['inverted_output'])
            iconOn = settings[index]['iconOn']
            iconOff = settings[index]['iconOff']
            confirmOff = bool(settings[index]['confirmOff'])

            # set the icon state
            GPIO.setup(relay_pin, GPIO.OUT)
            self.model[index]['relay_pin'] = relay_pin
            self.model[index]['state'] = GPIO.input(relay_pin) # int
            self.model[index]['labelText'] = labelText
            self.model[index]['active'] = active
            if inverted is not bool(self.model[index]['state']):
                self.model[index]['iconText'] = iconOn
                self.model[index]['confirmOff'] = confirmOff
            else:
                self.model[index]['iconText'] = iconOff
                self.model[index]['confirmOff'] = False

        #self._logger.info(f"update ui with model {self.model}")
        self._plugin_manager.send_plugin_message(self._identifier, self.model)

    def process_at_command(self, comm_instance, phase, command, parameters, tags=None, *args, **kwargs):
        if command == AT_COMMAND:
            index = parameters
            self.update_relay(index)
            return None

    def get_update_information(self):
        return {
            "octorelay": {
                "displayName": "OctoRelay",
                "displayVersion": self._plugin_version,
                "current": self._plugin_version,
                **UPDATES_CONFIG
            }
        }

    # GPIO Polling thread
    def input_polling(self):
        self._logger.debug("input_polling")
        for index in RELAY_INDEXES:
            # model::active is currently int, see update_ui()
            isActive = bool(self.model[index]['active'])
            modelState = self.model[index]['state'] # int
            actualState = GPIO.input(self.model[index]['relay_pin']) # int
            if isActive and actualState != modelState:
                self._logger.debug(f"relay: {index} has changed its pin state")
                self.update_ui()
                break

__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = OctoRelayPlugin()

__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config":
        __plugin_implementation__.get_update_information,
    "octoprint.access.permissions":
        __plugin_implementation__.get_additional_permissions,
    "octoprint.comm.protocol.atcommand.sending":
        __plugin_implementation__.process_at_command
}
from ._version import __version__