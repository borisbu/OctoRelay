# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from typing import Optional
from functools import reduce
import os
import time
import flask

import octoprint.plugin
from octoprint.events import Events
from octoprint.util import RepeatedTimer
from octoprint.access.permissions import Permissions

from .const import (
    get_default_settings, get_templates, get_ui_vars, RELAY_INDEXES, ASSETS, SWITCH_PERMISSION, UPDATES_CONFIG,
    POLLING_INTERVAL, UPDATE_COMMAND, GET_STATUS_COMMAND, LIST_ALL_COMMAND, AT_COMMAND, SETTINGS_VERSION,
    STARTUP, PRINTING_STOPPED, PRINTING_STARTED, CANCELLATION_EXCEPTIONS, PREEMPTIVE_CANCELLATION_CUTOFF,
    CANCEL_TASK_COMMAND, USER_ACTION
)
from .driver import Relay
from .task import Task
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
        self.tasks = [] # of Task
        self.model = { index: {} for index in RELAY_INDEXES }

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

    def get_template_vars(self):
        return get_ui_vars()

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
            CANCEL_TASK_COMMAND: [ "subject", "target", "owner" ]
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
            settings = self._settings.get([], merged=True) # expensive
            for index in RELAY_INDEXES:
                if settings[index]["active"]:
                    relay = Relay(
                        int(settings[index]["relay_pin"] or 0),
                        bool(settings[index]["inverted_output"])
                    )
                    active_relays.append({
                        "id": index,
                        "name": settings[index]["label_text"],
                        "active": relay.is_closed(),
                    })
            return flask.jsonify(active_relays)

        # API command to get relay status
        if command == GET_STATUS_COMMAND:
            settings = self._settings.get([data["pin"]], merged=True) # expensive
            relay = Relay(
                int(settings["relay_pin"] or 0),
                bool(settings["inverted_output"])
            )
            return flask.jsonify(status=relay.is_closed())

        # API command to toggle the relay
        if command == UPDATE_COMMAND:
            if not self.has_switch_permission():
                return flask.abort(403)
            index = data["pin"]
            if index not in RELAY_INDEXES:
                self._logger.warn(f"Invalid relay index supplied {index}")
                return flask.jsonify(status="error")
            self.toggle_relay(index)
            self.update_ui()
            return flask.jsonify(status="ok")

        # API command to cancel the postponed toggling task
        if command == CANCEL_TASK_COMMAND:
            self.cancel_tasks({
                **data, # {subject,target,owner}
                "initiator": USER_ACTION
            })
            self.update_ui()
        return flask.abort(400) # Unknown command

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
        settings = self._settings.get([], merged=True) # expensive
        for index in RELAY_INDEXES:
            if bool(settings[index]["active"]):
                target = settings[index]["rules"][event]["state"]
                if target is not None:
                    target = bool(target)
                    self.cancel_tasks({ "subject": index, "initiator": event })
                    delay = int(settings[index]["rules"][event]["delay"] or 0)
                    if delay == 0:
                        self.toggle_relay(index, target)
                    else:
                        task = Task(
                            subject = index,
                            target = target,
                            owner = event,
                            delay = delay,
                            function = self.toggle_relay,
                            args = [index, target]
                        )
                        self.tasks.append(task)
                        task.timer.start()

    def toggle_relay(self, index, target: Optional[bool] = None):
        settings = self._settings.get([index], merged=True) # expensive
        pin = int(settings["relay_pin"] or 0)
        inverted = bool(settings["inverted_output"])
        relay = Relay(pin, inverted)
        self._logger.debug(
            f"Toggling relay {index} on pin {pin}" if target is None else
            f"Turning the relay {index} {'ON' if target else 'OFF'} (pin {pin})"
        )
        cmd = settings["cmd_on" if relay.toggle(target) else "cmd_off"]
        self.run_system_command(cmd)

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.update_ui()

    def cancel_tasks(self, params: dict): # initiator, subject, target, owner
        exceptions = CANCELLATION_EXCEPTIONS.get(params.get("initiator")) or []
        target = params.get("target")
        owner = params.get("owner")
        def handler(task: Task):
            not_exception = task.owner not in exceptions
            same_subject = params.get("subject") == task.subject
            same_target = True if target is None else task.target == target
            same_owner = True if owner is None else task.owner == owner
            if same_subject and not_exception and same_target and same_owner:
                try:
                    task.timer.cancel()
                    self._logger.info(f"cancelled timer {task.owner} for relay {task.subject}")
                except Exception as exception:
                    self._logger.warn(
                        f"failed to cancel timer {task.owner} for {task.subject}, reason: {exception}"
                    )
                return False # exclude
            return True # include
        self.tasks = list(filter(handler, self.tasks))

    def run_system_command(self, cmd):
        if cmd:
            self._logger.info(f"OctoRelay runs system command: {cmd}")
            os.system(cmd)

    def get_upcoming_tasks(self):
        future_tasks = filter(
            lambda task: task.deadline > time.time() + PREEMPTIVE_CANCELLATION_CUTOFF,
            self.tasks
        )
        def reducer(agg, task):
            index = task.subject
            agg[index] = task if agg[index] is None or task.deadline < agg[index].deadline else agg[index]
            return agg
        return reduce( # { r1: task, r2: None, ... }
            reducer,
            future_tasks,
            { index: None for index in RELAY_INDEXES }
        )

    def update_ui(self):
        settings = self._settings.get([], merged=True) # expensive
        upcoming = self.get_upcoming_tasks()
        for index in RELAY_INDEXES:
            relay = Relay(
                int(settings[index]["relay_pin"] or 0),
                bool(settings[index]["inverted_output"])
            )
            relay_state = relay.is_closed()
            self.model[index] = {
                "relay_pin": relay.pin,
                "inverted_output": relay.inverted,
                "relay_state": relay_state, # bool since v3.1
                "label_text": settings[index]["label_text"],
                "active": bool(settings[index]["active"]),
                "icon_html": settings[index]["icon_on" if relay_state else "icon_off"],
                "confirm_off": bool(settings[index]["confirm_off"]) if relay_state else False,
                "upcoming": None if upcoming[index] is None else {
                    "target": upcoming[index].target,
                    "owner": upcoming[index].owner,
                    "deadline": int(upcoming[index].deadline * 1000) # ms for JS
                }
            }
        #self._logger.info(f"update ui with model {self.model}")
        self._plugin_manager.send_plugin_message(self._identifier, self.model)

    # pylint: disable=useless-return
    def process_at_command(self, _comm, _phase, command, parameters, *args, **kwargs):
        if command == AT_COMMAND:
            index = parameters
            if index in RELAY_INDEXES:
                self.toggle_relay(index)
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
        # self._logger.debug("input_polling") # in case your log file is too small
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
