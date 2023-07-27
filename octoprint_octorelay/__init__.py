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
        # pylint: disable=super-init-not-called
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
            self._logger.debug("settings for {}: {}".format(index, settings[index]))

            if settings[index]['active']:
                relay_pin = int(settings[index]['relay_pin'])
                initial_value = settings[index]['initial_value']
                inverted_output = settings[index]['inverted_output']

                # Setting the default state of pin
                GPIO.setup(relay_pin, GPIO.OUT)
                # XOR with inverted
                GPIO.output(relay_pin, initial_value != inverted_output)

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
        self._logger.debug("on_api_command {}, some_parameter is {}".format(command, data))

        # API command to get relay statuses
        if command == LIST_ALL_COMMAND:
            GPIO.setwarnings(False)
            activeRelays = []
            for index in RELAY_INDEXES:
                settings = self._settings.get([index], merged=True)
                if settings["active"]:
                    relay_pin = int(settings["relay_pin"])
                    inverted = settings['inverted_output']
                    GPIO.setup(relay_pin, GPIO.OUT)
                    relayData = {
                        "id": index,
                        "name": settings["labelText"],
                        "active": inverted != GPIO.input(relay_pin),
                    }
                    activeRelays.append(relayData)
            return flask.jsonify(activeRelays)

        # API command to get relay status
        if command == GET_STATUS_COMMAND:
            settings = self._settings.get([data["pin"]], merged=True)
            relay_pin = int(settings["relay_pin"])
            inverted = settings['inverted_output']
            GPIO.setwarnings(False)
            GPIO.setup(relay_pin, GPIO.OUT)
            relayState = inverted != GPIO.input(relay_pin)
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
            inverted = settings['inverted_output']
            cmdON = settings['cmdON']
            cmdOFF = settings['cmdOFF']

            GPIO.setwarnings(False)

            GPIO.setup(relay_pin, GPIO.OUT)
            # XOR with inverted
            relayState = inverted != GPIO.input(relay_pin)

            self._logger.debug("OctoRelay before pin: {}, inverted: {}, relayState: {}".format(
                relay_pin,
                inverted,
                relayState
            ))

            # toggle state
            relayState = not relayState

            GPIO.setup(relay_pin, GPIO.OUT)
            # XOR with inverted
            GPIO.output(relay_pin, inverted != relayState)

            GPIO.setwarnings(True)
            if relayState:
                if cmdON:
                    self._logger.info(
                        "OctoRelay system command: {}".format(cmdON))
                    os.system(cmdON)
            else:
                if cmdOFF:
                    self._logger.info(
                        "OctoRelay system command: {}".format(cmdOFF))
                    os.system(cmdOFF)
            self.update_ui()
            return "ok"
        except Exception as e:
            self._logger.debug(e)
            return "error"

    def on_event(self, event, payload):
        self._logger.debug("Got event: {}".format(event))
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
                self._logger.info("cancelled timer: {}".format(off_timer))
            except Exception:
                self._logger.warn("could not cancel timer: {}".format(off_timer))
        for index in RELAY_INDEXES:
            settings = self._settings.get([index], merged=True)

            relay_pin = int(settings["relay_pin"])
            inverted = settings['inverted_output']
            autoONforPrint = settings['autoONforPrint']
            cmdON = settings['cmdON']
            active = settings["active"]
            if autoONforPrint and active:
                self._logger.debug("turning on pin: {}, index: {}".format(relay_pin, index))
                self.turn_on_pin(relay_pin, inverted, cmdON)
        self.update_ui()

    def print_stopped(self):
        for index in RELAY_INDEXES:
            settings = self._settings.get([index], merged=True)

            relay_pin = int(settings["relay_pin"])
            inverted = settings['inverted_output']
            autoOFFforPrint = settings['autoOFFforPrint']
            autoOffDelay = int(settings['autoOffDelay'])
            cmdOFF = settings['cmdOFF']
            active = settings["active"]
            if autoOFFforPrint and active:
                self._logger.debug("turn off pin: {} in {} seconds. index: {}".format(
                    relay_pin, autoOffDelay, index))
                self.turn_off_timers[index] = ResettableTimer(
                    autoOffDelay, self.turn_off_pin, [relay_pin, inverted, cmdOFF])
                self.turn_off_timers[index].start()
        self.update_ui()

    def turn_off_pin(self, relay_pin, inverted, cmdOFF):
        GPIO.setup(relay_pin, GPIO.OUT)
        # XOR with inverted
        GPIO.output(relay_pin, inverted != False)
        GPIO.setwarnings(True)
        if cmdOFF:
            os.system(cmdOFF)
        self._logger.info("pin: {} turned off".format(relay_pin))
        self.update_ui()

    def turn_on_pin(self, relay_pin, inverted, cmdON):
        GPIO.setup(relay_pin, GPIO.OUT)
        # XOR with inverted
        GPIO.output(relay_pin, inverted == False)
        GPIO.setwarnings(True)
        if cmdON:
            os.system(cmdON)
        self._logger.info("pin: {} turned on".format(relay_pin))

    def update_ui(self):
        settings = DEFAULT_SETTINGS.copy()
        for index in RELAY_INDEXES:
            settings[index].update(self._settings.get([index]))

            labelText = settings[index]["labelText"]
            active = int(settings[index]["active"])
            relay_pin = int(settings[index]["relay_pin"])
            inverted = settings[index]['inverted_output']
            iconOn = settings[index]['iconOn']
            iconOff = settings[index]['iconOff']
            confirmOff = settings[index]['confirmOff']

            # set the icon state
            GPIO.setup(relay_pin, GPIO.OUT)
            self.model[index]['relay_pin'] = relay_pin
            self.model[index]['state'] = GPIO.input(relay_pin)
            self.model[index]['labelText'] = labelText
            self.model[index]['active'] = active
            if inverted != self.model[index]['state']:
                self.model[index]['iconText'] = iconOn
                self.model[index]['confirmOff'] = confirmOff
            else:
                self.model[index]['iconText'] = iconOff
                self.model[index]['confirmOff'] = False

        #self._logger.info("update ui with model {}".format(self.model))
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
            if self.model[index]['active'] and GPIO.input(self.model[index]['relay_pin']) != self.model[index]['state']:
                self._logger.debug("relay: {} has changed its pin state".format(index))
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
