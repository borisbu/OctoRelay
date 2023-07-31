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
GPIO_mock = Mock()
GPIO_mock.BCM = "MockedBCM"
GPIO_mock.OUT = "MockedOUT"
sys.modules["RPi.GPIO"] = GPIO_mock
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

    @classmethod
    def tearDownClass(cls):
        # Clean up
        del sys.modules["RPi.GPIO"]
        del sys.modules["octoprint.util"]
        del sys.modules["octoprint.access.permissions"]

    def test_constructor(self):
        # During the instantiation should configure GPIO and set initial values to certain props
        GPIO_mock.setmode.assert_called_with("MockedBCM")
        GPIO_mock.setwarnings.assert_called_with(False)
        self.assertIsNone(self.plugin_instance.polling_timer)
        self.assertEqual(self.plugin_instance.turn_off_timers, {})
        self.assertEqual(self.plugin_instance.model, {
            "r1": {}, "r2": {}, "r3": {}, "r4": {},
            "r5": {}, "r6": {}, "r7": {}, "r8": {}
        })

    def test_get_settings_defaults(self):
        expected = {
            "r1": {
                "active": True,
                "relay_pin": 4,
                "inverted_output": True,
                "initial_value": False,
                "cmdON": "",
                "cmdOFF": "",
                "iconOn": "&#128161;",
                "iconOff": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
                "labelText": "Light",
                "confirmOff": False,
                "autoONforPrint": True,
                "autoOFFforPrint": True,
                "autoOffDelay": 10,
            },
            "r2": {
                "active": True,
                "relay_pin": 17,
                "inverted_output": True,
                "initial_value": False,
                "cmdON": "",
                "cmdOFF": "",
                "iconOn": """<img width="24" height="24" src="/plugin/octorelay/static/img/3d-printer.svg">""",
                "iconOff": (
                    """<img width="24" height="24" src="/plugin/octorelay/static/img/3d-printer.svg" """
                    """style="filter: opacity(20%)">"""
                ),
                "labelText": "Printer",
                "confirmOff": True,
                "autoONforPrint": False,
                "autoOFFforPrint": False,
                "autoOffDelay": 0,
            },
            "r3": {
                "active": True,
                "relay_pin": 18,
                "inverted_output": True,
                "initial_value": False,
                "cmdON": "",
                "cmdOFF": "",
                "iconOn": """<img width="24" height="24" src="/plugin/octorelay/static/img/fan.svg" >""",
                "iconOff": (
                    """<img width="24" height="24" src="/plugin/octorelay/static/img/fan.svg" """
                    """style="filter: opacity(20%)">"""
                ),
                "labelText": "Fan",
                "confirmOff": False,
                "autoONforPrint": True,
                "autoOFFforPrint": True,
                "autoOffDelay": 10,
            },
            "r4": {
                "active": True,
                "relay_pin": 23,
                "inverted_output": True,
                "initial_value": True,
                "cmdON": "sudo service webcamd start",
                "cmdOFF": "sudo service webcamd stop",
                "iconOn": """<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" >""",
                "iconOff": (
                    """<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" """
                    """style="filter: opacity(20%)">"""
                ),
                "labelText": "Webcam",
                "confirmOff": False,
                "autoONforPrint": True,
                "autoOFFforPrint": True,
                "autoOffDelay": 10,
            },
            "r5": {
                "active": False,
                "relay_pin": 24,
                "inverted_output": True,
                "initial_value": False,
                "cmdON": "",
                "cmdOFF": "",
                "iconOn": "ON",
                "iconOff": "OFF",
                "labelText": "R5",
                "confirmOff": False,
                "autoONforPrint": False,
                "autoOFFforPrint": False,
                "autoOffDelay": 0,
            },
            "r6": {
                "active": False,
                "relay_pin": 25,
                "inverted_output": True,
                "initial_value": False,
                "cmdON": "",
                "cmdOFF": "",
                "iconOn": "&#128161;",
                "iconOff": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
                "labelText": "R6",
                "confirmOff": False,
                "autoONforPrint": False,
                "autoOFFforPrint": False,
                "autoOffDelay": 0,
            },
            "r7": {
                "active": False,
                "relay_pin": 8,
                "inverted_output": True,
                "initial_value": False,
                "cmdON": "",
                "cmdOFF": "",
                "iconOn": "&#128161;",
                "iconOff": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
                "labelText": "R7",
                "confirmOff": False,
                "autoONforPrint": False,
                "autoOFFforPrint": False,
                "autoOffDelay": 0,
            },
            "r8": {
                "active": False,
                "relay_pin": 7,
                "inverted_output": True,
                "initial_value": False,
                "cmdON": "",
                "cmdOFF": "",
                "iconOn": "&#128161;",
                "iconOff": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
                "labelText": "R8",
                "confirmOff": False,
                "autoONforPrint": False,
                "autoOFFforPrint": False,
                "autoOffDelay": 0,
            },
        }
        actual = self.plugin_instance.get_settings_defaults()
        self.assertEqual(actual, expected)

    def test_get_template_configs(self):
        expected = [
            { "type": "navbar", "custom_bindings": False },
            { "type": "settings", "custom_bindings": False }
        ]
        actual = self.plugin_instance.get_template_configs()
        self.assertEqual(actual, expected)

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
            "r1": { "active": 0, "relay_pin": 4, "state": 1 },
            "r2": { "active": 1, "relay_pin": 17, "state": 1 },
            "r3": { "active": 1, "relay_pin": 18, "state": 0 }
        }
        GPIO_mock.input = Mock(return_value=1)
        self.plugin_instance.input_polling()
        self.plugin_instance.update_ui.assert_called_with()
        self.plugin_instance._logger.debug.assert_called_with("relay: r3 has changed its pin state")

    def test_update_ui(self):
        # Should send message via plugin manager containing actual settings and the pins state
        GPIO_mock.input = Mock(return_value=0)
        cases = [
            { "inverted": True, "expectedIcon": "ON" },
            { "inverted": False, "expectedIcon": "OFF" }
        ]
        for case in cases:
            self.plugin_instance._settings.get = Mock(return_value={
                "active": True,
                "relay_pin": 17,
                "inverted_output": case["inverted"],
                "iconOn": "ON",
                "iconOff": "OFF",
                "labelText": "TEST",
                "confirmOff": False
            })
            expected_model = {}
            for index in self.plugin_instance.get_settings_defaults():
                expected_model[index] = {
                    "relay_pin": 17,
                    "state": 0,
                    "labelText": "TEST",
                    "active": 1,
                    "iconText": case["expectedIcon"],
                    "confirmOff": False
                }
            self.plugin_instance.update_ui()
            for index in self.plugin_instance.get_settings_defaults():
                self.plugin_instance._settings.get.assert_any_call([index])
            self.plugin_instance._plugin_manager.send_plugin_message.assert_called_with(
                "MockedIdentifier", expected_model
            )

    @patch("os.system")
    def test_turn_off_pin(self, system_mock):
        # Should set the pin state depending on inverted parameter and execute the supplied command
        self.plugin_instance.update_ui = Mock()
        cases = [
            { "inverted": True, "expectedOutput": True },
            { "inverted": False, "expectedOutput": False }
        ]
        for case in cases:
            self.plugin_instance.turn_off_pin(17, case["inverted"], "CommandMock")
            GPIO_mock.setup.assert_called_with(17, "MockedOUT")
            GPIO_mock.output.assert_called_with(17, case["expectedOutput"])
            GPIO_mock.setwarnings.assert_called_with(True)
            system_mock.assert_called_with("CommandMock")

    @patch("os.system")
    def test_turn_on_pin(self, system_mock):
        # Depending on relay type it should set its pin state and execute the supplied command
        cases = [
            { "inverted": True, "expectedOutput": False},
            { "inverted": False, "expectedOutput": True },
        ]
        for case in cases:
            self.plugin_instance.turn_on_pin(17, case["inverted"], "CommandMock")
            GPIO_mock.setup.assert_called_with(17, "MockedOUT")
            GPIO_mock.output.assert_called_with(17, case["expectedOutput"])
            GPIO_mock.setwarnings.assert_called_with(True)
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
            { "event": Events.PRINT_FAILED, "expectedMethod": self.plugin_instance.print_stopped }
        ]
        for case in cases:
            self.plugin_instance.on_event(case["event"], "MockedPayload")
            case["expectedMethod"].assert_called_with()

    def test_on_after_startup(self):
        # Depending on actual settings should set the pins state, update UI and start polling
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
                "initial_value": case["initial"]
            })
            self.plugin_instance.on_after_startup()
            GPIO_mock.setup.assert_called_with(17, "MockedOUT")
            GPIO_mock.output.assert_called_with(17, case["expectedOutput"])
            self.plugin_instance.update_ui.assert_called_with()
            utilMock.RepeatedTimer.assert_called_with(
                0.3, self.plugin_instance.input_polling, daemon = True
            )
            timerMock.start.assert_called_with()

    def test_print_started(self):
        # For relays configured with autoON should call turn_on_pin method and update UI
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.turn_off_timers = { "test": timerMock }
        cases = [
            { "autoOn": True, "inverted": True, "expectedCall": True},
            { "autoOn": True, "inverted": False, "expectedCall": True },
            { "autoOn": False, "inverted": True, "expectedCall": False },
            { "autoOn": False, "inverted": False, "expectedCall": False }
        ]
        for case in cases:
            self.plugin_instance.turn_on_pin = Mock()
            self.plugin_instance._settings.get = Mock(return_value={
                "active": True,
                "relay_pin": 17,
                "inverted_output": case["inverted"],
                "autoONforPrint": case["autoOn"],
                "cmdON": "CommandMock"
            })
            self.plugin_instance.print_started()
            timerMock.cancel.assert_called_with()
            if case["expectedCall"]:
                self.plugin_instance.turn_on_pin.assert_called_with(17, case["inverted"], "CommandMock")
            else:
                self.plugin_instance.turn_on_pin.assert_not_called()
            self.plugin_instance.update_ui.assert_called_with()

    def test_print_started__exception(self):
        # Should handle a possible exception when cancelling the timer
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.turn_off_timers = {
            "test": Mock(
                cancel=Mock( side_effect=Exception("Caught!") )
            )
        }
        self.plugin_instance.turn_on_pin = Mock()
        self.plugin_instance._settings.get = Mock(return_value={
            "active": False,
            "relay_pin": 17,
            "inverted_output": False,
            "autoONforPrint": False,
            "cmdON": None
        })
        self.plugin_instance.print_started()
        self.plugin_instance._logger.warn.assert_called_with("could not cancel timer: test, reason: Caught!")
        self.plugin_instance.turn_on_pin.assert_not_called()
        self.plugin_instance.update_ui.assert_called_with()

    def test_print_stopped(self):
        # For relays with autoOff feature should set timer to turn its pin off
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.turn_off_timers = { "r4": timerMock }
        cases = [
            { "autoOff": True, "expectedCall": True },
            { "autoOff": False, "expectedCall": False },
        ]
        for case in cases:
            utilMock.ResettableTimer.reset_mock()
            timerMock.start.reset_mock()
            self.plugin_instance._settings.get = Mock(return_value={
                "active": True,
                "relay_pin": 17,
                "inverted_output": False,
                "autoOFFforPrint": case["autoOff"],
                "autoOffDelay": 300,
                "cmdOFF": "CommandMock"
            })
            self.plugin_instance.print_stopped()
            if case["expectedCall"]:
                utilMock.ResettableTimer.assert_called_with(
                    300, self.plugin_instance.turn_off_pin, [17, False, "CommandMock"]
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
    def test_on_api_command(self, jsonify_mock, system_mock):
        # Depending on command should perform different actions and response with JSON
        self.plugin_instance.update_ui = Mock()
        GPIO_mock.input = Mock(return_value=1)
        cases = [
            {
                "command": "listAllStatus",
                "data": None,
                "inverted": True,
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
                "inverted": False,
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
                "inverted": True,
                "expectedStatus": False
            },
            {
                "command": "getStatus",
                "data": { "pin": "r4" },
                "inverted": False,
                "expectedStatus": True
            },
            {
                "command": "update",
                "data": { "pin": "r4" },
                "inverted": True,
                "expectedStatus": "ok",
                "expectedOutput": True,
                "expectedCommand": "CommandOnMock"
            },
            {
                "command": "update",
                "data": { "pin": "r4" },
                "inverted": False,
                "expectedStatus": "ok",
                "expectedOutput": False,
                "expectedCommand": "CommandOffMock"
            }
        ]
        for case in cases:
            permissionsMock.PLUGIN_OCTORELAY_SWITCH.can = Mock(return_value=True)
            self.plugin_instance._settings.get = Mock(return_value={
                "active": True,
                "relay_pin": 17,
                "inverted_output": case["inverted"],
                "labelText": "TEST",
                "cmdON": "CommandOnMock",
                "cmdOFF": "CommandOffMock"
            })
            self.plugin_instance.on_api_command(case["command"], case["data"])
            if case["command"] != "listAllStatus":
                self.plugin_instance._settings.get.assert_called_with(["r4"], merged=True)
            if hasattr(case, "expectedJson"):
                jsonify_mock.assert_called_with(case["expectedJson"])
            if hasattr(case, "expectedOutput"):
                GPIO_mock.output.assert_called_with("r4", case["expectedOutput"])
            if hasattr(case, "expectedCommand"):
                system_mock.assert_called_with(case["expectedCommand"])
            if hasattr(case, "expectedStatus"):
                jsonify_mock.assert_called_with(status=case["expectedStatus"])

    @patch("flask.abort")
    def test_on_api_command__exception(self, abort_mock):
        # Should refuse to update the pin state in case of insufficient permissions
        self.plugin_instance._settings.get = Mock(return_value={
            "active": True,
            "relay_pin": 17,
            "inverted_output": False,
            "cmdON": "CommandOnMock",
            "cmdOFF": "CommandOffMock"
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
