# -*- coding: utf-8 -*-
# pylint: disable=duplicate-code
# pylint: disable=too-many-public-methods
# pylint: disable=protected-access

import unittest
import sys
from unittest.mock import Mock, patch
from octoprint.events import Events
from octoprint.access import ADMIN_GROUP, USER_GROUP

# Patching required before importing OctoRelayPlugin class
sys.modules["RPi.GPIO"] = Mock()

# Mocks used for assertions
timerMock = Mock()
utilMock = Mock(
    RepeatedTimer = Mock(return_value=timerMock),
    ResettableTimer = Mock(return_value=timerMock)
)
sys.modules["octoprint.util"] = utilMock

permissionsMock = Mock()
sys.modules["octoprint.access.permissions"] = Mock(
    Permissions=permissionsMock
)

migrationsMock = Mock()
sys.modules["octoprint_octorelay.migrations"] = migrationsMock

relayMock = Mock()
relayConstructorMock = Mock(return_value=relayMock)
sys.modules["octoprint_octorelay.driver"] = Mock(
    Relay=relayConstructorMock
)

# pylint: disable=wrong-import-position
from octoprint_octorelay import OctoRelayPlugin, __plugin_pythoncompat__, __plugin_implementation__, __plugin_hooks__

class TestOctoRelayPlugin(unittest.TestCase):
    def setUp(self):
        # Create an instance of the OctoRelayPlugin class
        self.plugin_instance = OctoRelayPlugin()
        self.plugin_instance._identifier = "MockedIdentifier"
        self.plugin_instance._plugin_version = "MockedVersion"
        self.plugin_instance._logger = Mock()
        self.plugin_instance._settings = Mock()
        self.plugin_instance._plugin_manager = Mock()
        self.plugin_instance._printer = Mock()

    def test_constructor(self):
        # During the instantiation should set initial values to certain props
        self.assertIsNone(self.plugin_instance.polling_timer)
        self.assertEqual(self.plugin_instance.timers, [])
        self.assertEqual(self.plugin_instance.model, {
            "r1": {}, "r2": {}, "r3": {}, "r4": {},
            "r5": {}, "r6": {}, "r7": {}, "r8": {}
        })

    def test_get_settings_version(self):
        self.assertEqual(self.plugin_instance.get_settings_version(), 2)

    def test_get_settings_defaults(self):
        expected = {
            "r1": {
                "active": False,
                "relay_pin": 4,
                "inverted_output": True,
                "cmd_on": "",
                "cmd_off": "",
                "icon_on": "&#128161;",
                "icon_off": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
                "label_text": "Light",
                "confirm_off": False,
                "rules": {
                    "STARTUP": {
                        "state": False,
                    },
                    "PRINTING_STARTED": {
                        "state": True,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": False,
                        "delay": 10,
                    },
                },
            },
            "r2": {
                "active": False,
                "relay_pin": 17,
                "inverted_output": True,
                "cmd_on": "",
                "cmd_off": "",
                "icon_on": """<img width="24" height="24" src="/plugin/octorelay/static/img/3d-printer.svg">""",
                "icon_off": (
                    """<img width="24" height="24" src="/plugin/octorelay/static/img/3d-printer.svg" """
                    """style="filter: opacity(20%)">"""
                ),
                "label_text": "Printer",
                "confirm_off": True,
                "rules": {
                    "STARTUP": {
                        "state": False,
                    },
                    "PRINTING_STARTED": {
                        "state": None,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": None,
                        "delay": 0,
                    },
                },
            },
            "r3": {
                "active": False,
                "relay_pin": 18,
                "inverted_output": True,
                "cmd_on": "",
                "cmd_off": "",
                "icon_on": """<img width="24" height="24" src="/plugin/octorelay/static/img/fan.svg" >""",
                "icon_off": (
                    """<img width="24" height="24" src="/plugin/octorelay/static/img/fan.svg" """
                    """style="filter: opacity(20%)">"""
                ),
                "label_text": "Fan",
                "confirm_off": False,
                "rules": {
                    "STARTUP": {
                        "state": False,
                    },
                    "PRINTING_STARTED": {
                        "state": True,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": False,
                        "delay": 10,
                    },
                },
            },
            "r4": {
                "active": False,
                "relay_pin": 23,
                "inverted_output": True,
                "cmd_on": "sudo service webcamd start",
                "cmd_off": "sudo service webcamd stop",
                "icon_on": """<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" >""",
                "icon_off": (
                    """<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" """
                    """style="filter: opacity(20%)">"""
                ),
                "label_text": "Webcam",
                "confirm_off": False,
                "rules": {
                    "STARTUP": {
                        "state": True,
                    },
                    "PRINTING_STARTED": {
                        "state": True,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": False,
                        "delay": 10,
                    },
                },
            },
            "r5": {
                "active": False,
                "relay_pin": 24,
                "inverted_output": True,
                "cmd_on": "",
                "cmd_off": "",
                "icon_on": "ON",
                "icon_off": "OFF",
                "label_text": "R5",
                "confirm_off": False,
                "rules": {
                    "STARTUP": {
                        "state": False,
                    },
                    "PRINTING_STARTED": {
                        "state": None,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": None,
                        "delay": 0,
                    },
                },
            },
            "r6": {
                "active": False,
                "relay_pin": 25,
                "inverted_output": True,
                "cmd_on": "",
                "cmd_off": "",
                "icon_on": "&#128161;",
                "icon_off": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
                "label_text": "R6",
                "confirm_off": False,
                "rules": {
                    "STARTUP": {
                        "state": False,
                    },
                    "PRINTING_STARTED": {
                        "state": None,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": None,
                        "delay": 0,
                    },
                },
            },
            "r7": {
                "active": False,
                "relay_pin": 8,
                "inverted_output": True,
                "cmd_on": "",
                "cmd_off": "",
                "icon_on": "&#128161;",
                "icon_off": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
                "label_text": "R7",
                "confirm_off": False,
                "rules": {
                    "STARTUP": {
                        "state": False,
                    },
                    "PRINTING_STARTED": {
                        "state": None,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": None,
                        "delay": 0,
                    },
                },
            },
            "r8": {
                "active": False,
                "relay_pin": 7,
                "inverted_output": True,
                "cmd_on": "",
                "cmd_off": "",
                "icon_on": "&#128161;",
                "icon_off": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
                "label_text": "R8",
                "confirm_off": False,
                "rules": {
                    "STARTUP": {
                        "state": False,
                    },
                    "PRINTING_STARTED": {
                        "state": None,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": None,
                        "delay": 0,
                    },
                },
            },
        }
        actual = self.plugin_instance.get_settings_defaults()
        self.assertEqual(actual, expected)

    def test_get_settings_defaults__immutable(self):
        # Check that the function returns new object each time
        first = self.plugin_instance.get_settings_defaults()
        first["r1"]["relay_pin"] = 14
        second = self.plugin_instance.get_settings_defaults()
        self.assertEqual(first["r1"]["relay_pin"], 14)
        self.assertEqual(second["r1"]["relay_pin"], 4)

    def test_on_settings_migrate(self):
        # Should run the migrations
        self.plugin_instance._settings.get = Mock(return_value={})
        self.plugin_instance.on_settings_migrate(1, None)
        self.plugin_instance._logger.info.assert_any_call(
            "OctoRelay performs the migration of its settings from v0 to v1"
        )
        migrationsMock.migrate.assert_called_with(0, self.plugin_instance._settings, self.plugin_instance._logger)
        self.plugin_instance._logger.info.assert_called_with("OctoRelay finished the migration of settings to v1")

    def test_get_template_configs(self):
        expected = [
            { "type": "navbar", "custom_bindings": False },
            { "type": "settings", "custom_bindings": False }
        ]
        actual = self.plugin_instance.get_template_configs()
        self.assertEqual(actual, expected)

    def test_get_template_configs__immutable(self):
        # Check that the function returns new object each time
        first = self.plugin_instance.get_template_configs()
        first[0]["type"] = "test"
        second = self.plugin_instance.get_template_configs()
        self.assertEqual(first[0]["type"], "test")
        self.assertEqual(second[0]["type"], "navbar")

    def test_get_assets(self):
        expected = { "js": [ "js/octorelay.js" ] }
        actual = self.plugin_instance.get_assets()
        self.assertEqual(actual, expected)

    def test_get_api_commands(self):
        expected = { "update": [ "pin" ], "getStatus": [ "pin" ], "listAllStatus": [] }
        actual = self.plugin_instance.get_api_commands()
        self.assertEqual(actual, expected)

    def test_get_update_information(self):
        expected = {
            "octorelay": {
                "displayName": "OctoRelay",
                "displayVersion": "MockedVersion",
                "type": "github_release",
                "current": "MockedVersion",
                "user": "borisbu",
                "repo": "OctoRelay",
                "pip": "https://github.com/borisbu/OctoRelay/releases/download/{target}/release.zip",
                "stable_branch": {
                    "name": "Stable",
                    "branch": "master",
                    "commitish": [ "master" ]
                },
                "prerelease_branches": [{
                    "name": "Prerelease",
                    "branch": "develop",
                    "commitish": [ "develop", "master" ]
                }]
            }
        }
        actual = self.plugin_instance.get_update_information()
        self.assertEqual(actual, expected)

    def test_python_compatibility(self):
        self.assertEqual(__plugin_pythoncompat__, ">=3.7,<4")

    def test_exposed_implementation(self):
        self.assertIsInstance(__plugin_implementation__, OctoRelayPlugin)

    def test_exposed_hooks(self):
        expected = {
            "octoprint.plugin.softwareupdate.check_config":
                __plugin_implementation__.get_update_information,
            "octoprint.access.permissions":
                __plugin_implementation__.get_additional_permissions,
            "octoprint.comm.protocol.atcommand.sending":
                __plugin_implementation__.process_at_command
        }
        self.assertEqual(__plugin_hooks__, expected)

    def test_on_shutdown(self):
        self.plugin_instance.polling_timer = Mock()
        self.plugin_instance.on_shutdown()
        self.plugin_instance.polling_timer.cancel.assert_called_with()

    def test_input_polling(self):
        # First active relay having state not equal to the one stored in model should trigger UI update
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.model = {
            "r1": { "active": False, "relay_pin": 4, "inverted_output": False, "relay_state": True },
            "r2": { "active": True, "relay_pin": 17, "inverted_output": False, "relay_state": True },
            "r3": { "active": True, "relay_pin": 18, "inverted_output": False, "relay_state": False }
        }
        relayMock.is_closed = Mock(return_value=True)
        self.plugin_instance.input_polling()
        relayConstructorMock.assert_any_call(4, False)
        relayConstructorMock.assert_any_call(17, False)
        relayConstructorMock.assert_any_call(18, False)
        self.plugin_instance.update_ui.assert_called_with()
        self.plugin_instance._logger.debug.assert_called_with("relay: r3 has changed its pin state")

    def test_update_ui(self):
        # Should send message via plugin manager containing actual settings and the relay state
        cases = [
            { "closed": True, "expectedIcon": "ON" },
            { "closed": False, "expectedIcon": "OFF" }
        ]
        for case in cases:
            relayMock.pin = 17
            relayMock.inverted = False
            relayMock.is_closed = Mock(return_value=case["closed"])
            self.plugin_instance._settings.get = Mock(return_value={
                "active": True,
                "relay_pin": relayMock.pin,
                "inverted_output": False,
                "icon_on": "ON",
                "icon_off": "OFF",
                "label_text": "TEST",
                "confirm_off": False
            })
            expected_model = {}
            for index in self.plugin_instance.get_settings_defaults():
                expected_model[index] = {
                    "relay_pin": 17,
                    "inverted_output": False,
                    "relay_state": case["closed"],
                    "label_text": "TEST",
                    "active": True,
                    "icon_html": case["expectedIcon"],
                    "confirm_off": False
                }
            self.plugin_instance.update_ui()
            relayConstructorMock.assert_called_with(17, False)
            for index in self.plugin_instance.get_settings_defaults():
                self.plugin_instance._settings.get.assert_any_call([index], merged=True)
            self.plugin_instance._plugin_manager.send_plugin_message.assert_called_with(
                "MockedIdentifier", expected_model
            )

    @patch("os.system")
    def test_toggle_relay(self, system_mock):
        # Should turn the relay off and execute the supplied command
        cases = [
            { "target": True, "inverted": False },
            { "target": True, "inverted": True },
            { "target": False, "inverted": False },
            { "target": False, "inverted": True },
        ]
        for case in cases:
            self.plugin_instance._settings.get = Mock(return_value={
                "active": True,
                "relay_pin": 17,
                "inverted_output": case["inverted"],
                "cmd_on": "CommandON",
                "cmd_off": "CommandOFF"
            })
            self.plugin_instance.toggle_relay("r4", case["target"])
            relayConstructorMock.assert_called_with(17, case["inverted"])
            relayMock.toggle.assert_called_with(case["target"])
            system_mock.assert_called_with("CommandON" if case["target"] else "CommandOFF")

    @patch("os.system")
    def test_turn_on_relay(self, system_mock):
        # Should turn the relay on and execute the supplied command
        cases = [
            { "inverted": True, "expectedOutput": False},
            { "inverted": False, "expectedOutput": True },
        ]
        for case in cases:
            self.plugin_instance.turn_on_relay(17, case["inverted"], "CommandMock")
            relayConstructorMock.assert_called_with(17, case["inverted"])
            relayMock.close.assert_called_with()
            system_mock.assert_called_with("CommandMock")

    @patch("octoprint.plugin")
    def test_on_settings_save(self, plugins_mock):
        # Should call the SettingsPlugin event handler with own instance and supplied argument
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.on_settings_save("MockedData")
        plugins_mock.SettingsPlugin.on_settings_save.assert_called_with(
            self.plugin_instance, "MockedData"
        )
        self.plugin_instance.update_ui.assert_called_with()

    def test_on_event(self):
        # Depending on certain event type should call a corresponding method
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.print_started = Mock()
        self.plugin_instance.print_stopped = Mock()
        cases = [
            { "event": Events.CLIENT_OPENED, "expectedMethod": self.plugin_instance.update_ui },
            { "event": Events.PRINT_STARTED, "expectedMethod": self.plugin_instance.print_started },
            { "event": Events.PRINT_DONE, "expectedMethod": self.plugin_instance.print_stopped },
            { "event": Events.PRINT_FAILED, "expectedMethod": self.plugin_instance.print_stopped },

        ]
        if hasattr(Events, "CONNECTIONS_AUTOREFRESHED"): # Requires OctoPrint 1.9+
            cases.append({
                "event": Events.CONNECTIONS_AUTOREFRESHED,
                "expectedMethod": self.plugin_instance._printer.connect
            })
        for case in cases:
            self.plugin_instance.on_event(case["event"], "MockedPayload")
            case["expectedMethod"].assert_called_with()

    def test_on_after_startup(self):
        # Depending on actual settings should set the relay state, update UI and start polling
        self.plugin_instance.update_ui = Mock()
        cases = [
            { "inverted": True, "initial": True, "expectedOutput": False },
            { "inverted": True, "initial": False, "expectedOutput": True },
            { "inverted": False, "initial": True, "expectedOutput": True },
            { "inverted": False, "initial": False, "expectedOutput": False }
        ]
        for case in cases:
            self.plugin_instance._settings.get = Mock(return_value={
                "active": True,
                "relay_pin": 17,
                "inverted_output": case["inverted"],
                "rules": {
                    "STARTUP": { "state": case["initial"] }
                }
            })
            self.plugin_instance.on_after_startup()
            relayConstructorMock.assert_called_with(17, case["inverted"])
            relayMock.toggle.assert_called_with(case["initial"])
            self.plugin_instance.update_ui.assert_called_with()
            utilMock.RepeatedTimer.assert_called_with(
                0.3, self.plugin_instance.input_polling, daemon = True
            )
            timerMock.start.assert_called_with()

    def test_print_started(self):
        # For relays configured with autoON should call turn_on_relay method and update UI
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.timers = [{"subject": "r4", "timer": timerMock}]
        cases = [
            { "autoOn": True, "inverted": True, "expectedCall": True},
            { "autoOn": True, "inverted": False, "expectedCall": True },
            { "autoOn": False, "inverted": True, "expectedCall": False },
            { "autoOn": False, "inverted": False, "expectedCall": False }
        ]
        for case in cases:
            self.plugin_instance.turn_on_relay = Mock()
            self.plugin_instance._settings.get = Mock(return_value={
                "active": True,
                "relay_pin": 17,
                "inverted_output": case["inverted"],
                "auto_on_before_print": case["autoOn"],
                "cmd_on": "CommandMock"
            })
            self.plugin_instance.print_started()
            timerMock.cancel.assert_called_with()
            if case["expectedCall"]:
                self.plugin_instance.turn_on_relay.assert_called_with(17, case["inverted"], "CommandMock")
            else:
                self.plugin_instance.turn_on_relay.assert_not_called()
            self.plugin_instance.update_ui.assert_called_with()

    def test_print_started__exception(self):
        # Should handle a possible exception when cancelling the timer
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.timers = [{
            "subject": "r4",
            "timer": Mock(
                cancel=Mock( side_effect=Exception("Caught!") )
            )
        }]
        self.plugin_instance.turn_on_relay = Mock()
        self.plugin_instance._settings.get = Mock(return_value={
            "active": False,
            "relay_pin": 17,
            "inverted_output": False,
            "auto_on_before_print": False,
            "cmd_on": None
        })
        self.plugin_instance.print_started()
        self.plugin_instance._logger.warn.assert_called_with("failed to cancel timer 0 for r4, reason: Caught!")
        self.plugin_instance.turn_on_relay.assert_not_called()
        self.plugin_instance.update_ui.assert_called_with()

    def test_print_stopped(self):
        # For relays with autoOff feature should set timer to turn its pin off
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.timers = [{ "subject": "r4", "timer": timerMock }]
        cases = [
            { "state": False, "expectedCall": True },
            { "state": None, "expectedCall": False },
        ]
        for case in cases:
            utilMock.ResettableTimer.reset_mock()
            timerMock.start.reset_mock()
            self.plugin_instance._settings.get = Mock(return_value={
                "active": True,
                "relay_pin": 17,
                "inverted_output": False,
                "rules": {
                    "PRINTING_STOPPED": {
                        "state": case["state"],
                        "delay": 300
                    }
                },
                "cmd_off": "CommandMock"
            })
            self.plugin_instance.print_stopped()
            if case["expectedCall"]:
                utilMock.ResettableTimer.assert_called_with(
                    300, self.plugin_instance.toggle_relay, ["r8", False]
                )
                timerMock.start.assert_called_with()
            else:
                utilMock.ResettableTimer.assert_not_called()
                timerMock.start.assert_not_called()
            self.plugin_instance.update_ui.assert_called_with()

    def test_has_switch_permission(self):
        # Should proxy the permission and handle a possible exception
        cases = [
            { "mock": Mock(return_value=True), "expected": True },
            { "mock": Mock(return_value=False), "expected": False },
            { "mock": Mock(side_effect=Exception("Caught!")), "expected": False }
        ]
        for case in cases:
            permissionsMock.PLUGIN_OCTORELAY_SWITCH.can = case["mock"]
            actual = self.plugin_instance.has_switch_permission()
            permissionsMock.PLUGIN_OCTORELAY_SWITCH.can.assert_called_with()
            self.assertIs(actual, case["expected"])
        self.plugin_instance._logger.warn.assert_called_with("Failed to check relay switching permission, Caught!")

    @patch("flask.jsonify")
    @patch("os.system")
    def test_on_api_command(self, system_mock, jsonify_mock):
        # Depending on command should perform different actions and response with JSON
        self.plugin_instance.update_ui = Mock()
        cases = [
            {
                "command": "listAllStatus",
                "data": None,
                "closed": False,
                "expectedJson": [
                    { "id": "r1", "name": "TEST", "active": False },
                    { "id": "r2", "name": "TEST", "active": False },
                    { "id": "r3", "name": "TEST", "active": False },
                    { "id": "r4", "name": "TEST", "active": False },
                    { "id": "r5", "name": "TEST", "active": False },
                    { "id": "r6", "name": "TEST", "active": False },
                    { "id": "r7", "name": "TEST", "active": False },
                    { "id": "r8", "name": "TEST", "active": False }
                ]
            },
            {
                "command": "listAllStatus",
                "data": None,
                "closed": True,
                "expectedJson": [
                    { "id": "r1", "name": "TEST", "active": True },
                    { "id": "r2", "name": "TEST", "active": True },
                    { "id": "r3", "name": "TEST", "active": True },
                    { "id": "r4", "name": "TEST", "active": True },
                    { "id": "r5", "name": "TEST", "active": True },
                    { "id": "r6", "name": "TEST", "active": True },
                    { "id": "r7", "name": "TEST", "active": True },
                    { "id": "r8", "name": "TEST", "active": True }
                ]
            },
            {
                "command": "getStatus",
                "data": { "pin": "r4" },
                "closed": False,
                "expectedStatus": False
            },
            {
                "command": "getStatus",
                "data": { "pin": "r4" },
                "closed": True,
                "expectedStatus": True
            },
            {
                "command": "update",
                "data": { "pin": "r4" },
                "closed": False,
                "expectedStatus": "ok",
                "expectedToggle": True,
                "expectedCommand": "CommandOnMock"
            },
            {
                "command": "update",
                "data": { "pin": "r4" },
                "closed": True,
                "expectedStatus": "ok",
                "expectedToggle": True,
                "expectedCommand": "CommandOffMock"
            }
        ]
        for case in cases:
            relayMock.is_closed = Mock(return_value=case["closed"])
            relayMock.toggle = Mock(return_value=not case["closed"])
            permissionsMock.PLUGIN_OCTORELAY_SWITCH.can = Mock(return_value=True)
            self.plugin_instance._settings.get = Mock(return_value={
                "active": True,
                "relay_pin": 17,
                "inverted_output": False,
                "label_text": "TEST",
                "cmd_on": "CommandOnMock",
                "cmd_off": "CommandOffMock"
            })
            self.plugin_instance.on_api_command(case["command"], case["data"])
            if case["command"] != "listAllStatus":
                self.plugin_instance._settings.get.assert_called_with(["r4"], merged=True)
            if "expectedJson" in case:
                jsonify_mock.assert_called_with(case["expectedJson"])
            if "expectedToggle" in case:
                relayMock.toggle.assert_called_with()
            if "expectedCommand" in case:
                system_mock.assert_called_with(case["expectedCommand"])
            if "expectedStatus" in case:
                jsonify_mock.assert_called_with(status=case["expectedStatus"])

    @patch("flask.abort")
    def test_on_api_command__exception(self, abort_mock):
        # Should refuse to update the pin state in case of insufficient permissions
        self.plugin_instance._settings.get = Mock(return_value={
            "active": True,
            "relay_pin": 17,
            "inverted_output": False,
            "cmd_on": "CommandOnMock",
            "cmd_off": "CommandOffMock"
        })
        permissionsMock.PLUGIN_OCTORELAY_SWITCH.can = Mock(return_value=False)
        self.plugin_instance.on_api_command("update", { "pin": "r4" })
        permissionsMock.PLUGIN_OCTORELAY_SWITCH.can.assert_called_with()
        abort_mock.assert_called_with(403)

    @patch("flask.abort")
    def test_on_api_command__unknown(self, abort_mock):
        # Should respond with status code 400 (bad request) to unknown commands
        self.plugin_instance.on_api_command("command", {})
        abort_mock.assert_called_with(400)

    def test_update_relay__exception(self):
        # Should catch possible exceptions within try-catch block
        self.plugin_instance._settings.get = Mock(side_effect=Exception("Caught!"))
        actual = self.plugin_instance.update_relay("r4")
        self.assertEqual(actual, "error")
        self.plugin_instance._logger.warn.assert_called_with("OctoRelay update_relay caught an exception: Caught!")

    def test_process_at_command(self):
        # Should call update_relay() method with supplied parameter
        self.plugin_instance.update_relay = Mock()
        self.assertIsNone(self.plugin_instance.process_at_command(None, None, "OCTORELAY", "r4"))
        self.plugin_instance.update_relay.assert_called_with("r4")

    def test_get_additional_permissions(self):
        expected = [{
            "key": "SWITCH",
            "name": "Relay switching",
            "description": "Allows to switch GPIO pins and execute related OS commands.",
            "roles": [ "switch" ],
            "dangerous": False,
            "default_groups": [ ADMIN_GROUP, USER_GROUP ]
        }]
        actual = self.plugin_instance.get_additional_permissions()
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
