# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import flask
from RPi import GPIO

import octoprint.plugin
from octoprint.events import Events
from octoprint.util import ResettableTimer
from octoprint.util import RepeatedTimer
from octoprint.access.permissions import Permissions

from octoprint_octorelay.const import (
    get_default_settings, get_templates, RELAY_INDEXES, ASSETS, SWITCH_PERMISSION, UPDATES_CONFIG,
    POLLING_INTERVAL, UPDATE_COMMAND, GET_STATUS_COMMAND, LIST_ALL_COMMAND, AT_COMMAND
)
from octoprint_octorelay.driver import Relay

# pylint: disable=too-many-ancestors
# pylint: disable=too-many-instance-attributes
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
        return get_default_settings()

    def get_template_configs(self):
        return get_templates()

    def get_assets(self):
        return ASSETS

    def on_after_startup(self):
        self._logger.info("--------------------------------------------")
        self._logger.info("start OctoRelay")
        settings = get_default_settings()

        for index in RELAY_INDEXES:
            settings[index].update(self._settings.get([index]))
            self._logger.debug(f"settings for {index}: {settings[index]}")

            if settings[index]["active"]:
                relay_pin = int(settings[index]["relay_pin"])
                initial_value = bool(settings[index]["initial_value"])
                inverted_output = bool(settings[index]["inverted_output"])

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
        except Exception as exception:
            self._logger.warn(f"Failed to check relay switching permission, {exception}")
            return False

    def on_api_command(self, command, data):
        self._logger.debug(f"on_api_command {command}, parameters {data}")

        # API command to get relay statuses
        if command == LIST_ALL_COMMAND:
            GPIO.setwarnings(False)
            active_relays = []
            for index in RELAY_INDEXES:
                settings = self._settings.get([index], merged=True)
                if settings["active"]:
                    relay_pin = int(settings["relay_pin"])
                    inverted = bool(settings["inverted_output"])
                    GPIO.setup(relay_pin, GPIO.OUT)
                    active_relays.append({
                        "id": index,
                        "name": settings["labelText"],
                        "active": inverted is not bool(GPIO.input(relay_pin)),
                    })
            return flask.jsonify(active_relays)

        # API command to get relay status
        if command == GET_STATUS_COMMAND:
            settings = self._settings.get([data["pin"]], merged=True)
            relay_pin = int(settings["relay_pin"])
            inverted = bool(settings["inverted_output"])
            GPIO.setwarnings(False)
            GPIO.setup(relay_pin, GPIO.OUT)
            relay_state = inverted is not bool(GPIO.input(relay_pin))
            return flask.jsonify(status=relay_state)

        # API command to toggle the relay
        if command == UPDATE_COMMAND:
            if not self.has_switch_permission():
                return flask.abort(403)
            status = self.update_relay(data["pin"])
            return flask.jsonify(status=status)

        # Unknown command
        return flask.abort(400)

    def update_relay(self, index):
        try:
            settings = self._settings.get([index], merged=True)

            relay_pin = int(settings["relay_pin"])
            inverted = bool(settings["inverted_output"])
            cmd_on = settings["cmdON"]
            cmd_off = settings["cmdOFF"]

            GPIO.setwarnings(False)

            GPIO.setup(relay_pin, GPIO.OUT)
            # XOR with inverted
            relay_state = inverted is not bool(GPIO.input(relay_pin))

            self._logger.debug(f"OctoRelay before pin: {relay_pin}, inverted: {inverted}, relay_state: {relay_state}")

            # toggle state
            relay_state = not relay_state

            GPIO.setup(relay_pin, GPIO.OUT)
            # XOR with inverted
            GPIO.output(relay_pin, inverted is not relay_state)

            GPIO.setwarnings(True)
            if relay_state:
                if cmd_on:
                    self._logger.info(f"OctoRelay system command: {cmd_on}")
                    os.system(cmd_on)
            else:
                if cmd_off:
                    self._logger.info(f"OctoRelay system command: {cmd_off}")
                    os.system(cmd_off)
            self.update_ui()
            return "ok"
        except Exception as exception:
            self._logger.warn(f"OctoRelay update_relay caught an exception: {exception}")
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

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.update_ui()

    def print_started(self):
        for index, off_timer in self.turn_off_timers.items():
            try:
                off_timer.cancel()
                self._logger.info(f"cancelled timer: {index}")
            except Exception as exception:
                self._logger.warn(f"could not cancel timer: {index}, reason: {exception}")
        for index in RELAY_INDEXES:
            settings = self._settings.get([index], merged=True)

            relay_pin = int(settings["relay_pin"])
            inverted = bool(settings["inverted_output"])
            auto_on = bool(settings["autoONforPrint"])
            cmd_on = settings["cmdON"]
            active = bool(settings["active"])
            if auto_on and active:
                self._logger.debug(f"turning on pin: {relay_pin}, index: {index}")
                self.turn_on_pin(relay_pin, inverted, cmd_on)
        self.update_ui()

    def print_stopped(self):
        for index in RELAY_INDEXES:
            settings = self._settings.get([index], merged=True)

            relay_pin = int(settings["relay_pin"])
            inverted = bool(settings["inverted_output"])
            auto_off = bool(settings["autoOFFforPrint"])
            delay = int(settings["autoOffDelay"])
            cmd_off = settings["cmdOFF"]
            active = bool(settings["active"])
            if auto_off and active:
                self._logger.debug(f"turn off pin: {relay_pin} in {delay} seconds. index: {index}")
                self.turn_off_timers[index] = ResettableTimer(
                    delay, self.turn_off_pin, [relay_pin, inverted, cmd_off])
                self.turn_off_timers[index].start()
        self.update_ui()

    def turn_off_pin(self, relay_pin: int, inverted: bool, cmd):
        GPIO.setup(relay_pin, GPIO.OUT)
        # XOR with inverted
        GPIO.output(relay_pin, inverted is not False)
        GPIO.setwarnings(True)
        if cmd:
            os.system(cmd)
        self._logger.info(f"pin: {relay_pin} turned off")
        self.update_ui()

    def turn_on_pin(self, relay_pin: int, inverted: bool, cmd):
        GPIO.setup(relay_pin, GPIO.OUT)
        # XOR with inverted
        GPIO.output(relay_pin, inverted is False)
        GPIO.setwarnings(True)
        if cmd:
            os.system(cmd)
        self._logger.info(f"pin: {relay_pin} turned on")

    def update_ui(self):
        settings = get_default_settings()
        for index in RELAY_INDEXES:
            settings[index].update(self._settings.get([index]))

            relay_pin = int(settings[index]["relay_pin"])
            inverted = bool(settings[index]["inverted_output"])
            GPIO.setup(relay_pin, GPIO.OUT)
            pin_state = GPIO.input(relay_pin) # int
            relay_state = inverted is not bool(pin_state) # todo extract into some kind of driver later

            # set the icon state
            self.model[index]["relay_pin"] = relay_pin
            self.model[index]["state"] = pin_state # int
            self.model[index]["labelText"] = settings[index]["labelText"]
            self.model[index]["active"] = int(settings[index]["active"]) # todo make it bool later
            if relay_state:
                self.model[index]["iconText"] = settings[index]["iconOn"]
                self.model[index]["confirmOff"] = bool(settings[index]["confirmOff"])
            else:
                self.model[index]["iconText"] = settings[index]["iconOff"]
                self.model[index]["confirmOff"] = False

        #self._logger.info(f"update ui with model {self.model}")
        self._plugin_manager.send_plugin_message(self._identifier, self.model)

    # pylint: disable=useless-return
    def process_at_command(self, _comm, _phase, command, parameters, *args, **kwargs):
        if command == AT_COMMAND:
            index = parameters
            self.update_relay(index)
        return None # meaning no further actions required

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
            active = bool(self.model[index]["active"])
            model_state = self.model[index]["state"] # int
            actual_state = GPIO.input(self.model[index]["relay_pin"]) # int
            if active and actual_state != model_state:
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

# pylint: disable=wrong-import-position
from octoprint_octorelay._version import __version__
