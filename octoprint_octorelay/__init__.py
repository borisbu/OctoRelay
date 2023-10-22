# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from typing import Optional, List, Dict, Iterable
from functools import reduce
import os
import time
import flask

import octoprint.plugin
from octoprint.events import Events
from octoprint.util import RepeatedTimer, ResettableTimer
from octoprint.access.permissions import Permissions

from .const import (
    get_default_settings, get_templates, get_ui_vars, RELAY_INDEXES, ASSETS, SWITCH_PERMISSION, UPDATES_CONFIG,
    POLLING_INTERVAL, UPDATE_COMMAND, GET_STATUS_COMMAND, LIST_ALL_COMMAND, AT_COMMAND, SETTINGS_VERSION,
    STARTUP, PRINTING_STOPPED, PRINTING_STARTED, PRIORITIES, FALLBACK_PRIORITY, PREEMPTIVE_CANCELLATION_CUTOFF,
    CANCEL_TASK_COMMAND, USER_ACTION, TURNED_ON
)
from .driver import Relay
from .task import Task
from .migrations import migrate
from .model import Model, get_initial_model
from .exceptions import HandlingException

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
        self.tasks: List[Task] = []
        self.model: Model = get_initial_model()

    def get_settings_version(self):
        return SETTINGS_VERSION

    def get_settings_defaults(self):
        return get_default_settings()

    def on_settings_save(self, data):
        self._logger.info(f"Saving the settings: {data}")
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.update_ui()

    def on_settings_migrate(self, target: int, current):
        current = current or 0
        self._logger.info(f"Performing the settings migration from v{current} to v{target}")
        migrate(current, self._settings, self._logger)
        self._logger.debug(f"Finished the settings migration to v{target}")

    def get_template_configs(self):
        return get_templates()

    def get_template_vars(self):
        return get_ui_vars()

    def get_assets(self):
        return ASSETS

    def on_after_startup(self):
        self._logger.info("Starting the plugin")
        self.handle_plugin_event(STARTUP)
        self.update_ui()
        self.polling_timer = RepeatedTimer(POLLING_INTERVAL, self.input_polling, daemon=True)
        self.polling_timer.start()
        self._logger.debug("The plugin started")

    def on_shutdown(self):
        self._logger.debug("Stopping the plugin")
        if self.polling_timer:
            self.polling_timer.cancel()
        self._logger.info("The plugin stopped")

    def get_api_commands(self):
        return {
            UPDATE_COMMAND: [],
            GET_STATUS_COMMAND: [],
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

    def handle_list_all_command(self):
        self._logger.debug("Collecting information on all the relay states")
        active_relays = []
        settings = self._settings.get([], merged=True) # expensive
        for index in RELAY_INDEXES:
            if bool(settings[index]["active"]):
                relay = Relay(
                    int(settings[index]["relay_pin"] or 0),
                    bool(settings[index]["inverted_output"])
                )
                active_relays.append({
                    "id": index,
                    "name": settings[index]["label_text"],
                    "status": relay.is_closed(),
                })
        return active_relays

    def handle_get_status_command(self, index: str) -> bool:
        self._logger.debug(f"Getting the relay {index} state")
        settings = self._settings.get([index], merged=True) # expensive
        if not bool(settings["active"]):
            raise HandlingException(400)
        return Relay(
            int(settings["relay_pin"] or 0),
            bool(settings["inverted_output"])
        ).is_closed()

    def handle_update_command(self, index: str, target: Optional[bool] = None) -> bool:
        self._logger.debug(f"Requested to switch the relay {index} to {target}")
        if not self.has_switch_permission():
            self._logger.warn("Insufficient permissions")
            raise HandlingException(403)
        if index not in RELAY_INDEXES:
            self._logger.warn(f"Invalid relay index supplied: {index}")
            raise HandlingException(400)
        try:
            state = self.toggle_relay(index, target)
        except Exception as exception: # disabled relay
            raise HandlingException(400) from exception
        self.update_ui()
        return state

    def handle_cancel_task_command(self, subject: str, target: bool, owner: str) -> bool:
        self._logger.debug(f"Cancelling tasks from {owner} to switch the relay {subject} {'ON' if target else 'OFF'}")
        is_cancelled = self.cancel_tasks(subject, USER_ACTION, target, owner)
        self.update_ui()
        return is_cancelled

    def on_api_command(self, command, data):
        # pylint: disable=too-many-return-statements
        self._logger.info(f"Received the API command {command} with parameters: {data}")
        version = data.get("version") or data.get("v") or 1
        subject_param_name = "pin" if version == 1 else "subject"
        subject = data.get(subject_param_name)
        target = data.get("target")
        if command in [GET_STATUS_COMMAND, UPDATE_COMMAND] and subject is None:
            return flask.abort(400, description=f"Parameter {subject_param_name} is missing")
        # API command to get relay statuses
        if command == LIST_ALL_COMMAND:
            relays = self.handle_list_all_command()
            response = list(map(lambda item: {
                "id": item["id"],
                "name": item["name"],
                "active": item["status"]
            }, relays)) if version == 1 else relays # todo remove ternary branch when dropping v1
            self._logger.info(f"Responding {response} to {LIST_ALL_COMMAND} command")
            return flask.jsonify(response)
        # API command to get relay status
        if command == GET_STATUS_COMMAND:
            is_closed = False # todo remove this when dropping v1
            try:
                is_closed = self.handle_get_status_command(subject)
            except HandlingException as exception:
                if version != 1: # todo remove condition when dropping v1
                    return flask.abort(exception.status)
            self._logger.info(f"Responding {is_closed} to {GET_STATUS_COMMAND} command")
            return flask.jsonify({ "status": is_closed })
        # API command to toggle the relay
        if command == UPDATE_COMMAND:
            try:
                state = self.handle_update_command(subject, target if isinstance(target, bool) else None)
                self._logger.debug(f"Responding {state} to {UPDATE_COMMAND} command")
                if version == 1:
                    return flask.jsonify({ "status": "ok", "result": state }) # todo remove branch when dropping v1
                return flask.jsonify({ "status": state })
            except HandlingException as exception: # todo: deprecate the behavior for 400, only abort in next version
                if version == 1 and exception.status == 400:
                    return flask.jsonify({ "status": "error" }) # todo remove this branch when dropping v1
                return flask.abort(exception.status)
        # API command to cancel the postponed toggling task
        if command == CANCEL_TASK_COMMAND:
            cancelled = self.handle_cancel_task_command(
                data.get("subject"), bool(target), data["owner"] # todo use subject after dropping v1
            )
            self._logger.debug(f"Responding {cancelled} to {CANCEL_TASK_COMMAND} command")
            if version == 1:
                return flask.jsonify({ "status": "ok" }) # todo remove this branch when dropping v1
            return flask.jsonify({ "cancelled": cancelled })
        # Unknown commands
        self._logger.warn(f"Received unknown API command {command}")
        return flask.abort(400, description="Unknown command")

    def on_event(self, event, payload):
        self._logger.debug(f"Received the {event} event having payload: {payload}")
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
                if payload is not None and "ports" in payload and len(payload["ports"]) > 0:
                    delay = int(self._settings.get(["common", "delay"], merged=True) or 0) # expensive
                    self._logger.debug(f"AutoConnecting to the printer in {delay}s")
                    method = self._printer.connect
                    (method if delay == 0 else ResettableTimer(delay, method).start)()

    def handle_plugin_event(self, event, scope = None):
        if scope is None:
            scope = RELAY_INDEXES
        self._logger.debug(f"Handling the plugin event {event} having scope: {scope}")
        settings = self._settings.get([], merged=True) # expensive
        needs_ui_update = False
        for index in scope:
            if bool(settings[index]["active"]):
                did_cancel = self.cancel_tasks(subject = index, initiator = event) # issue 205
                needs_ui_update = needs_ui_update or did_cancel
                target = settings[index]["rules"][event]["state"]
                if target is not None:
                    target = bool(target)
                    if target and event == TURNED_ON:
                        self._logger.debug(f"Skipping {index} to avoid infinite loop")
                        continue # avoid infinite loop
                    delay = int(settings[index]["rules"][event]["delay"] or 0)
                    if delay == 0:
                        self.toggle_relay(index, target) # UI update conducted by the polling thread
                    else:
                        self._logger.debug(f"Postponing the switching of the relay {index} by {delay}s")
                        task = Task(
                            subject = index, target = target, owner = event, delay = delay,
                            function = self.toggle_relay, args = [index, target]
                        )
                        self.tasks.append(task)
                        task.timer.start()
                        self._logger.debug(f"The task registered: {task}")
                        needs_ui_update = True
        if needs_ui_update:
            self.update_ui() # issue 190

    def is_printer_relay(self, index) -> bool:
        printer_relay = self._settings.get(["common", "printer"], merged=True) # expensive
        return printer_relay is not None and printer_relay == index

    def toggle_relay(self, index, target: Optional[bool] = None) -> bool:
        settings = self._settings.get([index], merged=True) # expensive
        if not bool(settings["active"]):
            self._logger.warn(f"Relay {index} is disabled")
            raise Exception("Can not toggle a disabled relay")
        if target is not True and self.is_printer_relay(index):
            self._logger.debug(f"{index} is the printer relay")
            if self._printer.is_operational():
                self._logger.debug(f"Disconnecting from the printer before turning {index} OFF")
                self._printer.disconnect()
        pin = int(settings["relay_pin"] or 0)
        inverted = bool(settings["inverted_output"])
        relay = Relay(pin, inverted)
        self._logger.debug(
            f"Toggling the relay {index} on pin {pin}" if target is None else
            f"Turning the relay {index} {'ON' if target else 'OFF'} (pin {pin})"
        )
        state = relay.toggle(target)
        cmd = settings["cmd_on" if state else "cmd_off"]
        self.run_system_command(cmd)
        if state:
            self.handle_plugin_event(TURNED_ON, scope = [index])
        return state

    def cancel_tasks(
        self, subject: str, initiator: str,
        target: Optional[bool] = None, owner: Optional[str] = None
    ) -> bool: # returns True when cancelled some tasks
        self._logger.debug(f"Cancelling tasks by request from {initiator} for relay {subject}")
        priority = PRIORITIES.get(initiator) or FALLBACK_PRIORITY
        count_before = len(self.tasks)
        def handler(task: Task):
            lower_priority = (PRIORITIES.get(task.owner) or FALLBACK_PRIORITY) >= priority
            same_subject = subject == task.subject
            same_target = True if target is None else task.target == target
            same_owner = True if owner is None else task.owner == owner
            if same_subject and lower_priority and same_target and same_owner:
                try:
                    task.cancel_timer()
                    self._logger.info(f"Cancelled the task: {task}")
                except Exception as exception:
                    self._logger.warn(f"Failed to cancel {task}, reason: {exception}")
                return False # exclude
            return True # include
        self.tasks = list(filter(handler, self.tasks))
        count_cancelled = count_before - len(self.tasks)
        did_cancel = count_cancelled > 0
        self._logger.debug(
            f"Cancelled ({count_cancelled}) tasks and removed from the registry"
            if did_cancel else "No tasks cancelled"
        )
        return did_cancel

    def run_system_command(self, cmd):
        if cmd:
            self._logger.debug(f"Running the system command: {cmd}")
            os.system(cmd)

    def get_upcoming_tasks(self, subjects: Iterable[str]) -> Dict[str, Optional[Task]]:
        self._logger.debug("Finding the upcoming tasks")
        future_tasks = filter(
            lambda task: task.subject in subjects and task.deadline > time.time() + PREEMPTIVE_CANCELLATION_CUTOFF,
            self.tasks
        )
        def reducer(agg: Dict[str, Optional[Task]], task: Task):
            index = task.subject
            current = agg[index]
            agg[index] = task if current is None or task.deadline < current.deadline else current
            return agg
        return reduce( # { r1: task, r2: None, ... }
            reducer,
            future_tasks,
            { index: None for index in RELAY_INDEXES }
        )

    def update_ui(self):
        self._logger.debug("Updating the UI")
        settings = self._settings.get([], merged=True) # expensive
        upcoming_tasks = self.get_upcoming_tasks(filter(
            lambda index: bool(settings[index]["active"]) and bool(settings[index]["show_upcoming"]),
            RELAY_INDEXES
        ))
        for index in RELAY_INDEXES:
            active = bool(settings[index]["active"])
            relay = Relay(
                int(settings[index]["relay_pin"] or 0),
                bool(settings[index]["inverted_output"])
            )
            relay_state = relay.is_closed() if active else False
            task = upcoming_tasks[index]
            self.model[index] = {
                "relay_pin": relay.pin,
                "inverted_output": relay.inverted,
                "relay_state": relay_state, # bool since v3.1
                "label_text": settings[index]["label_text"],
                "active": active,
                "icon_html": settings[index]["icon_on" if relay_state else "icon_off"],
                "confirm_off": bool(settings[index]["confirm_off"]) if relay_state else False,
                "upcoming": None if task is None else {
                    "target": task.target,
                    "owner": task.owner,
                    "deadline": int(task.deadline * 1000) # ms for JS
                }
            }
        self._logger.debug(f"The UI feed: {self.model}")
        self._plugin_manager.send_plugin_message(self._identifier, self.model)

    # pylint: disable=useless-return
    def process_at_command(self, _comm, _phase, command, parameters, *args, **kwargs):
        self._logger.info(f"Received @{AT_COMMAND} command with params: {parameters}")
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
            ).is_closed() if active else False
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
