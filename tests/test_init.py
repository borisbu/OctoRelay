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
from octoprint_octorelay import (
    OctoRelayPlugin, __plugin_pythoncompat__, __plugin_implementation__,
    __plugin_hooks__, RELAY_INDEXES, Task, HandlingException
)

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
        self.assertEqual(self.plugin_instance.tasks, [])
        self.assertEqual(self.plugin_instance.model, {
            index: {
                "relay_pin": 0,
                "inverted_output": False,
                "relay_state": False,
                "label_text": index,
                "active": False,
                "icon_html": index,
                "confirm_off": False,
                "upcoming": None
            } for index in RELAY_INDEXES
        })

    def test_get_settings_version(self):
        # Should return the current version of settings defaults
        self.assertEqual(self.plugin_instance.get_settings_version(), 4)

    def test_get_settings_defaults(self):
        # Should return the plugin default settings
        expected = {
            "common": {
                "printer": "r2",
                "auto_connect_delay": 0
            },
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
                "show_upcoming": True,
                "rules": {
                    "STARTUP": {
                        "state": False,
                        "delay": 0,
                    },
                    "PRINTING_STARTED": {
                        "state": True,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": False,
                        "delay": 10,
                    },
                    "TURNED_ON": {
                        "state": None,
                        "delay": 0
                    }
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
                "show_upcoming": True,
                "rules": {
                    "STARTUP": {
                        "state": False,
                        "delay": 0,
                    },
                    "PRINTING_STARTED": {
                        "state": None,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": None,
                        "delay": 0,
                    },
                    "TURNED_ON": {
                        "state": None,
                        "delay": 0
                    }
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
                "show_upcoming": True,
                "rules": {
                    "STARTUP": {
                        "state": False,
                        "delay": 0,
                    },
                    "PRINTING_STARTED": {
                        "state": True,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": False,
                        "delay": 10,
                    },
                    "TURNED_ON": {
                        "state": None,
                        "delay": 0
                    }
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
                "show_upcoming": True,
                "rules": {
                    "STARTUP": {
                        "state": True,
                        "delay": 0,
                    },
                    "PRINTING_STARTED": {
                        "state": True,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": False,
                        "delay": 10,
                    },
                    "TURNED_ON": {
                        "state": None,
                        "delay": 0
                    }
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
                "show_upcoming": True,
                "rules": {
                    "STARTUP": {
                        "state": False,
                        "delay": 0,
                    },
                    "PRINTING_STARTED": {
                        "state": None,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": None,
                        "delay": 0,
                    },
                    "TURNED_ON": {
                        "state": None,
                        "delay": 0
                    }
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
                "show_upcoming": True,
                "rules": {
                    "STARTUP": {
                        "state": False,
                        "delay": 0,
                    },
                    "PRINTING_STARTED": {
                        "state": None,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": None,
                        "delay": 0,
                    },
                    "TURNED_ON": {
                        "state": None,
                        "delay": 0
                    }
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
                "show_upcoming": True,
                "rules": {
                    "STARTUP": {
                        "state": False,
                        "delay": 0,
                    },
                    "PRINTING_STARTED": {
                        "state": None,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": None,
                        "delay": 0,
                    },
                    "TURNED_ON": {
                        "state": None,
                        "delay": 0
                    }
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
                "show_upcoming": True,
                "rules": {
                    "STARTUP": {
                        "state": False,
                        "delay": 0,
                    },
                    "PRINTING_STARTED": {
                        "state": None,
                        "delay": 0,
                    },
                    "PRINTING_STOPPED": {
                        "state": None,
                        "delay": 0,
                    },
                    "TURNED_ON": {
                        "state": None,
                        "delay": 0
                    }
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
        self.plugin_instance._logger.info.assert_any_call("Performing the settings migration from v0 to v1")
        migrationsMock.migrate.assert_called_with(0, self.plugin_instance._settings, self.plugin_instance._logger)
        self.plugin_instance._logger.debug.assert_called_with("Finished the settings migration to v1")

    def test_get_template_configs(self):
        # Should return the plugin template configurations
        expected = [
            { "type": "navbar", "custom_bindings": False },
            { "type": "settings", "custom_bindings": False }
        ]
        actual = self.plugin_instance.get_template_configs()
        self.assertEqual(actual, expected)

    def test_get_template_vars(self):
        # Should return the variables needed for the settings template
        expected = {
            "events": {
                "STARTUP": { "label": "on Startup", "disabled": [] },
                "PRINTING_STARTED": { "label": "on Printing Started", "disabled": [] },
                "PRINTING_STOPPED": { "label": "on Printing Stopped", "disabled": [] },
                "TURNED_ON": { "label": "after Turned ON", "disabled": [ "true" ] }
            },
            "boolean": {
                "true": { "caption": "YES", "color": "info" },
                "false": { "caption": "NO", "color": "default" }
            },
            "tristate": {
                "true": { "caption": "ON", "color": "success" },
                "false": { "caption": "OFF", "color": "danger" },
                "null": { "caption": "skip", "color": "default" },
            }
        }
        actual = self.plugin_instance.get_template_vars()
        self.assertEqual(actual, expected)

    def test_get_template_configs__immutable(self):
        # Check that the function returns new object each time
        first = self.plugin_instance.get_template_configs()
        first[0]["type"] = "test"
        second = self.plugin_instance.get_template_configs()
        self.assertEqual(first[0]["type"], "test")
        self.assertEqual(second[0]["type"], "navbar")

    def test_get_assets(self):
        # Should return the plugin assets configutation
        expected = { "js": [ "js/octorelay.js" ], "css": [ "css/octorelay.css" ] }
        actual = self.plugin_instance.get_assets()
        self.assertEqual(actual, expected)

    def test_get_api_commands(self):
        # Should return the list of available plugin commands
        expected = {
            "update": [ "subject" ],
            "getStatus": [ "subject" ],
            "listAllStatus": [],
            "cancelTask": [ "subject", "target", "owner" ]
        }
        actual = self.plugin_instance.get_api_commands()
        self.assertEqual(actual, expected)

    def test_get_update_information(self):
        # Should return the update strategy configuration
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
        # Should be the current Python compability string
        self.assertEqual(__plugin_pythoncompat__, ">=3.7,<4")

    def test_exposed_implementation(self):
        # Should be an instance of the plugin class
        self.assertIsInstance(__plugin_implementation__, OctoRelayPlugin)

    def test_exposed_hooks(self):
        # Should be an object having handlers associated to the certain OctoPrint hooks
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
        # Should stop the polling timer
        self.plugin_instance.polling_timer = Mock()
        self.plugin_instance.on_shutdown()
        self.plugin_instance.polling_timer.cancel.assert_called_with()

    def test_input_polling(self):
        # First active relay having state not equal to the one stored in model should trigger UI update
        self.plugin_instance.update_ui = Mock()
        relayConstructorMock.reset_mock()
        self.plugin_instance.model = {
            "r1": { "active": False, "relay_pin": 4, "inverted_output": False, "relay_state": True },
            "r2": { "active": True, "relay_pin": 17, "inverted_output": False, "relay_state": True },
            "r3": { "active": True, "relay_pin": 18, "inverted_output": False, "relay_state": False }
        }
        relayMock.is_closed = Mock(return_value=True)
        self.plugin_instance.input_polling()
        self.assertEqual(relayConstructorMock.call_count, 2)
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
                index: {
                    "active": True,
                    "relay_pin": relayMock.pin,
                    "inverted_output": False,
                    "icon_on": "ON",
                    "icon_off": "OFF",
                    "label_text": "TEST",
                    "confirm_off": False,
                    "show_upcoming": True
                } for index in RELAY_INDEXES
            })
            expected_model = {}
            for index in RELAY_INDEXES:
                expected_model[index] = {
                    "relay_pin": 17,
                    "inverted_output": False,
                    "relay_state": case["closed"],
                    "label_text": "TEST",
                    "active": True,
                    "icon_html": case["expectedIcon"],
                    "confirm_off": False,
                    "upcoming": None
                }
            self.plugin_instance.update_ui()
            relayConstructorMock.assert_called_with(17, False)
            for index in RELAY_INDEXES:
                self.plugin_instance._settings.get.assert_any_call([], merged=True)
            self.plugin_instance._plugin_manager.send_plugin_message.assert_called_with(
                "MockedIdentifier", expected_model
            )

    def test_is_printer_relay(self):
        # Should assert the equality of the common/printer value with the supplied argument
        cases = [
            { "printer": "r4", "expected": True },
            { "printer": "r5", "expected": False },
            { "printer": None, "expected": False }
        ]
        for case in cases:
            self.plugin_instance._settings.get = Mock(return_value=case["printer"])
            actual = self.plugin_instance.is_printer_relay("r4")
            self.assertEqual(actual, case["expected"])

    @patch("os.system")
    def test_toggle_relay(self, system_mock):
        # Should toggle the relay and execute a command matching its new state
        self.plugin_instance.is_printer_relay = Mock(return_value=False)
        cases = [
            { "target": True, "inverted": False, "expectedCommand": "CommandON" },
            { "target": True, "inverted": True, "expectedCommand": "CommandON" },
            { "target": False, "inverted": False, "expectedCommand": "CommandOFF" },
            { "target": False, "inverted": True, "expectedCommand": "CommandOFF" },
            # in these cases the resulting relay state is mocked with the "inverted" value:
            { "target": None, "inverted": False, "expectedCommand": "CommandOFF" },
            { "target": None, "inverted": True, "expectedCommand": "CommandON" }
        ]
        for case in cases:
            self.plugin_instance.handle_plugin_event = Mock()
            relayMock.toggle = Mock(
                return_value=case["inverted"] if case["target"] is None else case["target"]
            )
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
            system_mock.assert_called_with(case["expectedCommand"])
            if case["expectedCommand"] == "CommandON":
                self.plugin_instance.handle_plugin_event.assert_called_with("TURNED_ON", scope = ["r4"])
            else:
                self.plugin_instance.handle_plugin_event.assert_not_called()

    def test_toggle_relay__disabled(self):
        # Should raise an exception when attempting to toggle a disabled relay
        relayMock.toggle = Mock()
        self.plugin_instance._settings.get = Mock(return_value={
            "active": False,
            "relay_pin": 17,
            "inverted_output": False,
            "cmd_on": "CommandON",
            "cmd_off": "CommandOFF"
        })
        with self.assertRaises(Exception):
            self.plugin_instance.toggle_relay("r4", True)
        relayMock.toggle.assert_not_called()

    def test_toggle_relay__printer(self):
        # Should disconnect from the printer when turning its relay off
        cases = [
            { "target": None, "is_printer": True, "is_operational": True },
            { "target": False, "is_printer": True, "is_operational": True },
            { "target": True, "is_printer": True, "is_operational": True },
            { "target": False, "is_printer": True, "is_operational": False },
            { "target": False, "is_printer": False, "is_operational": True },
        ]
        self.plugin_instance._settings.get = Mock(return_value={
            "active": True,
            "relay_pin": 17,
            "inverted_output": False,
            "cmd_on": None,
            "cmd_off": None
        })
        relayMock.toggle = Mock(return_value=False)
        for case in cases:
            self.plugin_instance._printer.reset_mock()
            self.plugin_instance.is_printer_relay = Mock(return_value=case["is_printer"])
            self.plugin_instance._printer.is_operational = Mock(return_value=case["is_operational"])
            self.plugin_instance.toggle_relay("r4", case["target"])
            if case["target"] is not True and case["is_printer"] and case["is_operational"]:
                self.plugin_instance._printer.disconnect.assert_called_with()
            else:
                self.plugin_instance._printer.disconnect.assert_not_called()

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
        self.plugin_instance.handle_plugin_event = Mock()
        cases = [
            {
                "event": Events.CLIENT_OPENED,
                "payload": {"remoteAddress": "127.0.0.1"},
                "expectedMethod": self.plugin_instance.update_ui,
                "expectedParams": []
            },
            {
                "event": Events.PRINT_STARTED,
                "payload": {"name": "test.gcode"},
                "expectedMethod": self.plugin_instance.handle_plugin_event,
                "expectedParams": ["PRINTING_STARTED"]
            },
            {
                "event": Events.PRINT_DONE,
                "payload": {"name": "test.gcode"},
                "expectedMethod": self.plugin_instance.handle_plugin_event,
                "expectedParams": ["PRINTING_STOPPED"]
            },
            {
                "event": Events.PRINT_FAILED,
                "payload": {"name": "test.gcode"},
                "expectedMethod": self.plugin_instance.handle_plugin_event,
                "expectedParams": ["PRINTING_STOPPED"]
            },
        ]
        if hasattr(Events, "CONNECTIONS_AUTOREFRESHED"): # Requires OctoPrint 1.9+
            cases.append({
                "event": Events.CONNECTIONS_AUTOREFRESHED,
                "payload": {"ports": ["/dev/ttyUSB0"]},
                "delay": 0,
                "expectedMethod": self.plugin_instance._printer.connect,
                "expectedParams": []
            })
            cases.append({
                "event": Events.CONNECTIONS_AUTOREFRESHED,
                "payload": {"ports": ["/dev/ttyUSB0"]},
                "delay": 5,
                "expectedMethod": utilMock.ResettableTimer,
                "expectedParams": [5, self.plugin_instance._printer.connect]
            })
        for case in cases:
            if "delay" in case:
                self.plugin_instance._settings.get = Mock(return_value=case["delay"])
            self.plugin_instance.on_event(case["event"], case["payload"])
            case["expectedMethod"].assert_called_with(*case["expectedParams"])

    def test_on_after_startup(self):
        # Should trigger STARTUP event handler, update UI and start polling
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.handle_plugin_event = Mock()
        self.plugin_instance.on_after_startup()
        self.plugin_instance.handle_plugin_event.assert_called_with("STARTUP")
        self.plugin_instance.update_ui.assert_called_with()
        utilMock.RepeatedTimer.assert_called_with(
            0.3, self.plugin_instance.input_polling, daemon = True
        )
        timerMock.start.assert_called_with()

    def test_handle_plugin_event(self):
        # Should follow the rule on handling the event by toggling the relay if "state" is not None
        self.plugin_instance.tasks = [{"subject": "r4", "timer": timerMock}]
        cases = [
            { "event": "PRINTING_STARTED", "state": True, "expectedCall": True, "delay": 300 },
            { "event": "PRINTING_STARTED", "state": False, "expectedCall": True, "delay": 300 },
            { "event": "PRINTING_STARTED", "state": None, "expectedCall": False, "delay": 300 },
            { "event": "PRINTING_STOPPED", "state": True, "expectedCall": True, "delay": 300 },
            { "event": "PRINTING_STOPPED", "state": False, "expectedCall": True, "delay": 300 },
            { "event": "PRINTING_STOPPED", "state": None, "expectedCall": False, "delay": 300 },
            { "event": "STARTUP", "state": True, "expectedCall": True, "delay": 300 },
            { "event": "STARTUP", "state": False, "expectedCall": True, "delay": 300 },
            { "event": "STARTUP", "state": None, "expectedCall": False, "delay": 300 },
            { "event": "TURNED_ON", "state": True, "expectedCall": False, "delay": 300 },
            { "event": "TURNED_ON", "state": False, "expectedCall": True, "delay": 300 },
            { "event": "TURNED_ON", "state": None, "expectedCall": False, "delay": 300 },
            { "event": "STARTUP", "state": True, "expectedCall": True, "delay": 0 },
            { "event": "STARTUP", "state": False, "expectedCall": True, "delay": 0 },
        ]
        for case in cases:
            self.plugin_instance.update_ui = Mock()
            self.plugin_instance.cancel_tasks = Mock(return_value=False)
            self.plugin_instance.tasks = []
            utilMock.ResettableTimer.reset_mock()
            timerMock.start.reset_mock()
            self.plugin_instance.toggle_relay = Mock()
            self.plugin_instance._settings.get = Mock(return_value={
                index: {
                    "active": True,
                    "rules": {
                        case["event"]: {
                            "state": case["state"],
                            "delay": case["delay"],
                        }
                    },
                } for index in RELAY_INDEXES
            })
            self.plugin_instance.handle_plugin_event(case["event"])
            self.plugin_instance.cancel_tasks.assert_called_with(subject = "r8", initiator = case["event"])
            if case["expectedCall"]:
                if case["delay"] == 0:
                    self.plugin_instance.toggle_relay.assert_called_with("r8", case["state"])
                else:
                    utilMock.ResettableTimer.assert_called_with(
                        case["delay"], self.plugin_instance.toggle_relay, ["r8", case["state"]]
                    )
                    timerMock.start.assert_called_with()
                    self.plugin_instance.update_ui.assert_called_with() # issue 190
                    self.assertEqual(len(self.plugin_instance.tasks), 8)
                    for index in range(0,8):
                        self.assertIsInstance(self.plugin_instance.tasks[index], Task)
                        self.assertEqual(self.plugin_instance.tasks[index].subject, f"r{index + 1}")
                        self.assertEqual(self.plugin_instance.tasks[index].owner, case["event"])
                        self.assertEqual(self.plugin_instance.tasks[index].delay, case["delay"])
                        self.assertEqual(self.plugin_instance.tasks[index].target, case["state"])
            else:
                utilMock.ResettableTimer.assert_not_called()
                timerMock.start.assert_not_called()
                self.plugin_instance.toggle_relay.assert_not_called()
                self.plugin_instance.update_ui.assert_not_called()

    def test_cancel_tasks(self):
        # Should remove the tasks for the certain relay and cancel its timer
        task1 = Task(subject = "r4", target = False, owner = "PRINTING_STOPPED", delay = 0, function=Mock(), args=[])
        task2 = Task(subject = "r6", target = False, owner = "PRINTING_STOPPED", delay = 0, function=Mock(), args=[])
        task3 = Task(subject = "r4", target = False, owner = "STARTUP", delay = 0, function = Mock(), args = [])
        cases = [
            { "initiator": "PRINTING_STARTED", "expected_rest": [ task2 ], "expected_call": True },
            # event having lower priority:
            { "initiator": "TURNED_ON", "expected_rest": [ task1, task2, task3 ], "expected_call": False },
            # event having higher priority:
            { "initiator": "USER_ACTION", "expected_rest": [ task2 ], "expected_call": False }
        ]
        for case in cases:
            timerMock.reset_mock()
            self.plugin_instance.tasks = [ task1, task2, task3 ]
            actual = self.plugin_instance.cancel_tasks(subject = "r4", initiator = case["initiator"])
            self.assertEqual(self.plugin_instance.tasks, case["expected_rest"])
            self.assertEqual(actual, len(case["expected_rest"]) < 3)
            if case["expected_call"]:
                timerMock.cancel.assert_called_with()

    def test_cancel_tasks__exception(self):
        # Should handle a possible exception when cancelling a timer
        self.plugin_instance.tasks = [
            Task(subject = "r4", target = False, owner = "PRINTING_STOPPED", delay = 0, function = Mock(), args = [])
        ]
        timerMock.cancel=Mock( side_effect=Exception("Caught!") )
        actual = self.plugin_instance.cancel_tasks(subject = "r4", initiator = "PRINTING_STARTED")
        self.plugin_instance._logger.warn.assert_called_with(
            "Failed to cancel Task(r4,False,PRINTING_STOPPED,0), reason: Caught!"
        )
        self.assertTrue(actual)
        timerMock.reset_mock()

    @patch("time.time", Mock(return_value=500))
    def test_get_upcoming_tasks(self):
        remaining_r4 = Task(
            subject = "r4",
            target = False,
            owner = "PRINTING_STARTED",
            delay = 1000,
            function = Mock(),
            args = []
        )
        remaining_r6 = Task(
            subject = "r6",
            target = False,
            owner = "PRINTING_STOPPED",
            delay = 2000,
            function = Mock(),
            args = []
        )
        self.plugin_instance.tasks = [
            Task(subject = "r4", target = False, owner = "PRINTING_STOPPED", delay = 2000, function = Mock(), args=[]),
            remaining_r6,
            remaining_r4,
            Task(subject = "r4", target = False, owner = "STARTUP", delay = -500, function = Mock(), args = [])
        ]
        actual = self.plugin_instance.get_upcoming_tasks(["r4", "r5", "r6"])
        self.assertEqual(actual, {
            "r1": None,
            "r2": None,
            "r3": None,
            "r4": remaining_r4,
            "r5": None,
            "r6": remaining_r6,
            "r7": None,
            "r8": None
        })

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

    def test_handle_list_all_command(self):
        # Should return the active relay states
        cases = [{
            "closed": False,
            "expectedJson": list(map(lambda index: {
                "id": index,
                "name": "TEST",
                "status": False
            }, RELAY_INDEXES))
        }, {
            "closed": True,
            "expectedJson": list(map(lambda index: {
                "id": index,
                "name": "TEST",
                "status": True
            }, RELAY_INDEXES))
        }]
        for case in cases:
            relayMock.is_closed = Mock(return_value=case["closed"])
            relay_settings_mock = {
                "active": True,
                "relay_pin": 17,
                "inverted_output": False,
                "label_text": "TEST",
                "cmd_on": "CommandOnMock",
                "cmd_off": "CommandOffMock"
            }
            self.plugin_instance._settings.get = Mock(return_value={
                index: relay_settings_mock for index in RELAY_INDEXES
            })
            self.assertEqual(
                self.plugin_instance.handle_list_all_command(),
                case["expectedJson"]
            )

    def test_handle_get_status_command(self):
        # Should return the relay state
        cases = [
            { "closed": False, "expectedStatus": False },
            { "closed": True, "expectedStatus": True }
        ]
        for case in cases:
            relayMock.is_closed = Mock(return_value=case["closed"])
            relay_settings_mock = {
                "active": True,
                "relay_pin": 17,
                "inverted_output": False,
                "label_text": "TEST",
                "cmd_on": "CommandOnMock",
                "cmd_off": "CommandOffMock"
            }
            self.plugin_instance._settings.get = Mock(return_value=relay_settings_mock)
            self.assertEqual(
                self.plugin_instance.handle_get_status_command("r4"),
                case["expectedStatus"]
            )
            self.plugin_instance._settings.get.assert_called_with(["r4"], merged=True)

    def test_handle_get_status_command__exception(self):
        # Should raise when requesting the state of disabled relay
        relay_settings_mock = {
            "active": False,
            "relay_pin": 17,
            "inverted_output": False,
            "label_text": "TEST",
            "cmd_on": "CommandOnMock",
            "cmd_off": "CommandOffMock"
        }
        self.plugin_instance._settings.get = Mock(return_value=relay_settings_mock)
        with self.assertRaises(HandlingException):
            self.plugin_instance.handle_get_status_command("r4")

    @patch("os.system")
    def test_handle_update_command(self, system_mock):
        # Should toggle the relay state, execute command, update UI and return the resulting state
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.is_printer_relay = Mock(return_value=False)
        cases = [
            {
                "index": "r4",
                "target": None,
                "closed": False,
                "expectedError": False,
                "expectedResult": True,
                "expectedToggle": True,
                "expectedCommand": "CommandOnMock",
                "expectedEvent": "TURNED_ON"
            },
            {
                "index": "r4",
                "target": False,
                "closed": True,
                "expectedError": False,
                "expectedResult": False, # from the !closed returned by mocked Relay::toggle() below
                "expectedToggle": True,
                "expectedCommand": "CommandOffMock"
            },
            {
                "index": "invalid",
                "target": False,
                "closed": True,
                "expectedError": True,
            }
        ]
        for case in cases:
            self.plugin_instance.handle_plugin_event = Mock()
            self.plugin_instance.update_ui.reset_mock()
            relayMock.is_closed = Mock(return_value=case["closed"])
            relayMock.toggle = Mock(return_value=not case["closed"])
            permissionsMock.PLUGIN_OCTORELAY_SWITCH.can = Mock(return_value=True)
            relay_settings_mock = {
                "active": True,
                "relay_pin": 17,
                "inverted_output": False,
                "label_text": "TEST",
                "cmd_on": "CommandOnMock",
                "cmd_off": "CommandOffMock"
            }
            self.plugin_instance._settings.get = Mock(return_value=relay_settings_mock)
            if case["expectedError"]:
                with self.assertRaises(HandlingException):
                    self.plugin_instance.handle_update_command(case["index"], case["target"])
            else:
                self.assertEqual(
                    self.plugin_instance.handle_update_command(case["index"], case["target"]),
                    case["expectedResult"]
                )
                self.plugin_instance._settings.get.assert_called_with(["r4"], merged=True)
            if "expectedToggle" in case:
                relayMock.toggle.assert_called_with(case["target"])
                self.plugin_instance.update_ui.assert_called_with()
            if "expectedCommand" in case:
                system_mock.assert_called_with(case["expectedCommand"])
            if "expectedEvent" in case:
                self.plugin_instance.handle_plugin_event.assert_called_with(case["expectedEvent"], scope = ["r4"])
            else:
                self.plugin_instance.handle_plugin_event.assert_not_called()

    def test_handle_update_command__exception_permissions(self):
        # Should raise in case of insufficient permissions
        self.plugin_instance._settings.get = Mock(return_value={
            "active": True,
            "relay_pin": 17,
            "inverted_output": False,
            "cmd_on": "CommandOnMock",
            "cmd_off": "CommandOffMock"
        })
        permissionsMock.PLUGIN_OCTORELAY_SWITCH.can = Mock(return_value=False)
        with self.assertRaises(HandlingException):
            self.plugin_instance.handle_update_command("r4")
        permissionsMock.PLUGIN_OCTORELAY_SWITCH.can.assert_called_with()

    def test_handle_update_command__exception_disabled(self):
        # Should raise when attempting to update a disabled relay
        self.plugin_instance._settings.get = Mock(return_value={
            "active": False,
            "relay_pin": 17,
            "inverted_output": False,
            "cmd_on": "CommandOnMock",
            "cmd_off": "CommandOffMock"
        })
        permissionsMock.PLUGIN_OCTORELAY_SWITCH.can = Mock(return_value=True)
        with self.assertRaises(HandlingException):
            self.plugin_instance.handle_update_command("r4")
        permissionsMock.PLUGIN_OCTORELAY_SWITCH.can.assert_called_with()

    def test_handle_cancel_task_command(self):
        # Should return boolean indicating that the task was cancelled
        self.plugin_instance.update_ui = Mock()
        self.plugin_instance.cancel_tasks = Mock()
        self.assertTrue(
            self.plugin_instance.handle_cancel_task_command("r4", True, "STARTUP")
        )
        self.plugin_instance.cancel_tasks.assert_called_with("r4", "USER_ACTION", True, "STARTUP")
        self.plugin_instance.update_ui.assert_called_with()

    @patch("flask.jsonify")
    def test_on_api_command(self, jsonify_mock):
        # Should call a handler and respond with expected payload
        self.plugin_instance.handle_list_all_command = Mock(return_value=[
            {"id": "r1", "name": "Test", "status": True}
        ])
        self.plugin_instance.handle_get_status_command = Mock(return_value=True)
        self.plugin_instance.handle_update_command = Mock(return_value=False)
        self.plugin_instance.handle_cancel_task_command = Mock(return_value=True)
        cases = [
            {
                "command": "listAllStatus",
                "data": {},
                "expectedMethod": self.plugin_instance.handle_list_all_command,
                "expectedArguments": [],
                "expectedOutcome": jsonify_mock,
                "expectedPayload": [{"id": "r1", "name": "Test", "status": True}],
            },
            {
                "command": "getStatus",
                "data": { "subject": "r4" },
                "expectedMethod": self.plugin_instance.handle_get_status_command,
                "expectedArguments": ["r4"],
                "expectedOutcome": jsonify_mock,
                "expectedPayload": {"status": True},
            },
            {
                "command": "update",
                "data": { "subject": "r4", "target": True },
                "expectedMethod": self.plugin_instance.handle_update_command,
                "expectedArguments": ["r4", True],
                "expectedOutcome": jsonify_mock,
                "expectedPayload": {"status": False},
            },
            {
                "command": "cancelTask",
                "data": { "subject": "r4", "owner": "STARTUP", "target": True },
                "expectedMethod": self.plugin_instance.handle_cancel_task_command,
                "expectedArguments": [ "r4", True, "STARTUP" ],
                "expectedOutcome": jsonify_mock,
                "expectedPayload": {"cancelled": True},
            }
        ]
        for case in cases:
            case["expectedMethod"].reset_mock()
            case["expectedOutcome"].reset_mock()
            self.plugin_instance.on_api_command(case["command"], case["data"])
            case["expectedMethod"].assert_called_with(*case["expectedArguments"])
            case["expectedOutcome"].assert_called_with(case["expectedPayload"])

    @patch("flask.abort")
    def test_on_api_command__update_exceptions(self, abort_mock):
        # Should respond with a faulty HTTP code when handler raises
        cases = [
            {
                "payload": { "subject": "r4" },
                "status": 403,
                "expectedCode": 403
            },
            {
                "payload": { "subject": "r4" },
                "status": 400,
                "expectedCode": 400
            }
        ]
        for case in cases:
            abort_mock.reset_mock()
            self.plugin_instance.handle_update_command = Mock(side_effect=HandlingException(case["status"]))
            self.plugin_instance.on_api_command("update", case["payload"])
            abort_mock.assert_called_with(case["expectedCode"])

    @patch("flask.abort")
    def test_om_api_command__get_status_exception(self, abort_mock):
        # Should respond with status false when handler raises
        self.plugin_instance.handle_get_status_command = Mock(side_effect=HandlingException(400))
        abort_mock.reset_mock()
        self.plugin_instance.on_api_command("getStatus", { "subject": "r4" })
        abort_mock.assert_called_with(400)

    @patch("flask.abort")
    def test_on_api_command__unknown(self, abort_mock):
        # Should respond with status code 400 (bad request) to unknown commands
        self.plugin_instance.on_api_command("command", {})
        abort_mock.assert_called_with(400, description="Unknown command")

    def test_process_at_command(self):
        # Should toggle or switch the relay having index and optional target supplied as a parameters
        self.plugin_instance.toggle_relay = Mock()
        cases = [
            { "params": "r4", "expected": ["r4", None] },
            { "params": "r4 ON", "expected": ["r4", True] },
            { "params": " r4  off  ", "expected": ["r4", False] },
            { "params": " r4  ...  ", "expected": ["r4", None] }
        ]
        for case in cases:
            self.plugin_instance.toggle_relay.reset_mock()
            self.assertIsNone(self.plugin_instance.process_at_command(None, None, "OCTORELAY", case["params"]))
            self.plugin_instance.toggle_relay.assert_called_with(*case["expected"])

    def test_get_additional_permissions(self):
        # Should return the list of the plugin custom permissions
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
