import unittest
import sys
from unittest.mock import Mock, patch, MagicMock
import os

# Patch RPi.GPIO module before importing OctoRelayPlugin class
GPIO_mock = Mock()
GPIO_mock.BCM = "MockedBCM"
GPIO_mock.OUT = "MockedOUT"
sys.modules['RPi.GPIO'] = GPIO_mock

from __init__ import OctoRelayPlugin
from __init__ import __plugin_pythoncompat__, __plugin_implementation__, __plugin_hooks__, POLLING_INTERVAL

class TestOctoRelayPlugin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create an instance of the OctoRelayPlugin class
        cls.plugin_instance = OctoRelayPlugin()
        cls.plugin_instance._plugin_version = "MockedVersion"
        cls.plugin_instance._logger = Mock()
        cls.plugin_instance._settings = Mock()

    @classmethod
    def tearDownClass(cls):
        # Clean up
        del sys.modules['RPi.GPIO']

    def test_GPIO_initialization(self):
        GPIO_mock.setmode.assert_called_with("MockedBCM")
        GPIO_mock.setwarnings.assert_called_with(False)

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
                "iconOff": """<img width="24" height="24" src="/plugin/octorelay/static/img/3d-printer.svg" style="filter: opacity(20%)">""",
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
                "iconOff": """<img width="24" height="24" src="/plugin/octorelay/static/img/fan.svg" style="filter: opacity(20%)">""",
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
                "iconOff": """<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" style="filter: opacity(20%)">""",
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
        expected = { "update": [], "getStatus": [], "listAllStatus": [] }
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
                "pip": "https://github.com/borisbu/OctoRelay/archive/{target}.zip",
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
                __plugin_implementation__.get_update_information
        }
        self.assertEqual(__plugin_hooks__, expected)

    def test_exposed_polling_interval(self):
        self.assertEqual(POLLING_INTERVAL, 0.3)

    def test_on_shutdown(self):
        self.plugin_instance.polling_timer = Mock()
        self.plugin_instance.on_shutdown()
        self.plugin_instance.polling_timer.cancel.assert_called_with()

    def test_input_polling(self):
        # First active relay having state not equal to the one stored in model should trigger UI update
        originalUpdate = self.plugin_instance.update_ui
        self.plugin_instance.model = {
            "r1": { "active": False, "relay_pin": 4, "state": True },
            "r2": { "active": True, "relay_pin": 17, "state": True },
            "r3": { "active": True, "relay_pin": 18, "state": False }
        }
        self.plugin_instance.update_ui = Mock()
        GPIO_mock.input = Mock(return_value=True)
        self.plugin_instance.input_polling()
        self.plugin_instance.update_ui.assert_called_with()
        self.plugin_instance._logger.debug.assert_called_with("relay: r3 has changed its pin state")
        self.plugin_instance.update_ui = originalUpdate

    def test_update_ui(self):
        self.plugin_instance.update_ui()
        settingValueMock = {
            "active": True,
            "relay_pin": 17,
            "inverted_output": True,
            "iconOn": "ON",
            "iconOff": "OFF",
            "labelText": "TEST",
            "confirmOff": False
        }
        self.plugin_instance._settings.get = Mock(return_value=settingValueMock)
        self.plugin_instance._settings.get.assert_called_with(["r1"])

if __name__ == '__main__':
    unittest.main()
