# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import flask
from typing import Optional

import octoprint.plugin
from octoprint.events import Events
from octoprint.util import ResettableTimer
from octoprint.util import RepeatedTimer
from octoprint.access.permissions import Permissions

from .const import (
    get_default_settings, get_templates, RELAY_INDEXES, ASSETS, SWITCH_PERMISSION, UPDATES_CONFIG,
    POLLING_INTERVAL, UPDATE_COMMAND, GET_STATUS_COMMAND, LIST_ALL_COMMAND, AT_COMMAND, SETTINGS_VERSION,
    STARTUP, PRINTING_STOPPED, PRINTING_STARTED
)
from .driver import Relay
from .migrations import migrate

# pylint: disable=too-many-ancestors
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
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
        self.polling_timer = None
        self.timers = [] # of { subject: relayIndex, timer: ResettableTimer }
        self.model = {}
        for index in RELAY_INDEXES:
            self.model[index] = {}

    def get_settings_version(self):
        return SETTINGS_VERSION

    def get_settings_defaults(self):
        return get_default_settings()

    def on_settings_migrate(self, target: int, current):
        current = current or 0
        self._logger.info(f"OctoRelay performs the migration of its settings from v{current} to v{target}")
        migrate(current, self._settings, self._logger)
        self._logger.info(f"OctoRelay finished the migration of settings to v{target}")

    def get_template_configs(self):
        return get_templates()

    def get_assets(self):
        return ASSETS

    def on_after_startup(self):
        self._logger.info("--------------------------------------------")
        self._logger.info("start OctoRelay")
        self.handle_plugin_event(STARTUP)
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
            active_relays = []
            for index in RELAY_INDEXES:
                settings = self._settings.get([index], merged=True)
                if settings["active"]:
                    relay = Relay(
                        int(settings["relay_pin"]),
                        bool(settings["inverted_output"])
                    )
                    active_relays.append({
                        "id": index,
                        "name": settings["label_text"],
                        "active": relay.is_closed(),
                    })
            return flask.jsonify(active_relays)

        # API command to get relay status
        if command == GET_STATUS_COMMAND:
            settings = self._settings.get([data["pin"]], merged=True)
            relay = Relay(
                int(settings["relay_pin"]),
                bool(settings["inverted_output"])
            )
            return flask.jsonify(status=relay.is_closed())

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
            relay = Relay(
                int(settings["relay_pin"]),
                bool(settings["inverted_output"])
            )
            cmd_on = settings["cmd_on"]
            cmd_off = settings["cmd_off"]
            self._logger.debug(f"OctoRelay before update {relay}")
            self.run_system_command(cmd_on if relay.toggle() else cmd_off) # ternary choice based on new state
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
            self.handle_plugin_event(PRINTING_STARTED)
        elif event == Events.PRINT_DONE:
            self.handle_plugin_event(PRINTING_STOPPED)
        elif event == Events.PRINT_FAILED:
            self.handle_plugin_event(PRINTING_STOPPED)
        elif hasattr(Events, "CONNECTIONS_AUTOREFRESHED"): # Requires OctoPrint 1.9+
            if event == Events.CONNECTIONS_AUTOREFRESHED:
                self._printer.connect()
        #elif event == Events.PRINT_CANCELLING:
            # self.print_stopped()
        #elif event == Events.PRINT_CANCELLED:
            # self.print_stopped()

    def handle_plugin_event(self, event):
        self.cancel_timers() # todo: which ones?
        for index in RELAY_INDEXES:
            settings = self._settings.get([index], merged=True)
            if bool(settings["active"]):
                target = settings["rules"][event]["state"]
                if target is not None:
                    delay = int(settings["rules"][event]["delay"])
                    timer = ResettableTimer(delay, self.toggle_relay, [index, bool(target)])
                    self.timers.append({
                        "subject": index,
                        "timer": timer
                    })
                    timer.start()

    # todo: should update ui?
    # todo: reuse by update_relay()
    def toggle_relay(self, index, target: Optional[bool] = None):
        settings = self._settings.get([index], merged=True)
        pin = int(settings["relay_pin"])
        inverted = bool(settings["inverted_output"])
        relay = Relay(pin, inverted)
        cmd = settings["cmd_on" if relay.toggle(target) else "cmd_off"]
        self.run_system_command(cmd)

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.update_ui()

    # todo: all of them?
    def cancel_timers(self):
        for index, entry in enumerate(self.timers):
            try:
                entry["timer"].cancel()
                self._logger.info(f"cancelled timer {index} for relay {entry['subject']}")
            except Exception as exception:
                self._logger.warn(f"failed to cancel timer {index} for {entry['subject']}, reason: {exception}")
            self.timers.pop(index)

    def run_system_command(self, cmd):
        if cmd:
            self._logger.info(f"OctoRelay runs system command: {cmd}")
            os.system(cmd)

    def update_ui(self):
        for index in RELAY_INDEXES:
            settings = self._settings.get([index], merged=True)
            relay = Relay(
                int(settings["relay_pin"]),
                bool(settings["inverted_output"])
            )
            relay_state = relay.is_closed()
            # set the icon state
            self.model[index]["relay_pin"] = relay.pin
            self.model[index]["inverted_output"] = relay.inverted
            self.model[index]["relay_state"] = relay_state # bool since v3.1
            self.model[index]["label_text"] = settings["label_text"]
            self.model[index]["active"] = bool(settings["active"])
            if relay_state:
                self.model[index]["icon_html"] = settings["icon_on"]
                self.model[index]["confirm_off"] = bool(settings["confirm_off"])
            else:
                self.model[index]["icon_html"] = settings["icon_off"]
                self.model[index]["confirm_off"] = False

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

    # Polling thread
    def input_polling(self):
        self._logger.debug("input_polling")
        for index in RELAY_INDEXES:
            active = self.model[index]["active"]
            model_state = self.model[index]["relay_state"] # bool since v3.1
            actual_state = Relay(
                self.model[index]["relay_pin"],
                self.model[index]["inverted_output"]
            ).is_closed()
            if active and (actual_state is not model_state):
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
from ._version import __version__
