# -*- coding: utf-8 -*-
# pylint: disable=duplicate-code
import unittest
import sys
from unittest.mock import Mock

# Revert mocking by test_init.py
if "octoprint_octorelay.migrations" in sys.modules:
    del sys.modules["octoprint_octorelay.migrations"]

# Mocking required before the further import
sys.modules["RPi.GPIO"] = Mock()

# pylint: disable=wrong-import-position
from octoprint_octorelay.const import SETTINGS_VERSION
from octoprint_octorelay.migrations import migrators, migrate, v0, v1, v2

# avoid keeping other modules automatically imported by this test
del sys.modules["octoprint_octorelay"]
del sys.modules["octoprint_octorelay.driver"]
del sys.modules["octoprint_octorelay.task"]

class TestMigrations(unittest.TestCase):
    def test_migrators__quantity(self):
        # Sould match the settings version
        self.assertEqual(len(migrators), SETTINGS_VERSION)

    def test_v0(self):
        # Should set first 4 relays active=True if active is not set
        settings = Mock(
            get = Mock(return_value={"relay_pin": 17})
        )
        logger = Mock()
        v0(settings, logger)
        for index in ["r1", "r2", "r3", "r4"]:
            settings.set.assert_any_call([index], {
                "relay_pin": 17,
                "active": True
            })

    def test_v1(self):
        # Should rename camel case settings to snake one
        settings = Mock(
            get = Mock(return_value={
                "active": False,
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
            })
        )
        logger = Mock()
        v1(settings, logger)
        for index in ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]:
            settings.set.assert_any_call([index], {
                "active": False,
                "relay_pin": 23,
                "inverted_output": True,
                "initial_value": True,
                "cmd_on": "sudo service webcamd start",
                "cmd_off": "sudo service webcamd stop",
                "icon_on": """<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" >""",
                "icon_off": (
                    """<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" """
                    """style="filter: opacity(20%)">"""
                ),
                "label_text": "Webcam",
                "confirm_off": False,
                "auto_on_before_print": True,
                "auto_off_after_print": True,
                "auto_off_delay": 10,
            })

    def test_v2(self):
        cases = [
            {
                "feed": {
                    "initial_value": True,
                    "auto_on_before_print": True,
                    "auto_off_after_print": True,
                    "auto_off_delay": 10,
                },
                "expected_startup_state": True,
                "expected_printing_started_state": True,
                "expected_printing_stopped_state": False,
            }, {
                "feed": {
                    "initial_value": False,
                    "auto_on_before_print": False,
                    "auto_off_after_print": False,
                    "auto_off_delay": 0,
                },
                "expected_startup_state": False,
                "expected_printing_started_state": None,
                "expected_printing_stopped_state": None,
            }
        ]
        for case in cases:
            settings = Mock(
                get=Mock(return_value={
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
                    **case["feed"]
                })
            )
            logger = Mock()
            v2(settings, logger)
            for index in ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]:
                settings.set.assert_any_call([index], {
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
                            "state": case["expected_startup_state"],
                            "delay": 0
                        },
                        "PRINTING_STARTED": {
                            "state": case["expected_printing_started_state"],
                            "delay": 0
                        },
                        "PRINTING_STOPPED": {
                            "state": case["expected_printing_stopped_state"],
                            "delay": case["feed"]["auto_off_delay"]
                        }
                    }
                })

    def test_migrate(self):
        # Should call all migrations
        settings = Mock(
            get = Mock(return_value={})
        )
        logger = Mock()
        migrate(0, settings, logger)
        logger.info.assert_any_call("Migrating the settings to v1")


if __name__ == "__main__":
    unittest.main()
