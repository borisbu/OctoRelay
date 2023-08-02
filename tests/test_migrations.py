# -*- coding: utf-8 -*-
import unittest
import sys
from unittest.mock import Mock

if "RPi.GPIO" in sys.modules:
    GPIO_mock = sys.modules["RPi.GPIO"]
else:
    GPIO_mock = Mock()
    GPIO_mock.BCM = "MockedBCM"
    GPIO_mock.OUT = "MockedOUT"
    sys.modules["RPi.GPIO"] = GPIO_mock

# pylint: disable=wrong-import-position
from octoprint_octorelay.const import SETTINGS_VERSION
from octoprint_octorelay.migrations import migrators, migrate, to_v1
del sys.modules["octoprint_octorelay"] # avoid keeping __init__.py imported in this test

class TestMigrations(unittest.TestCase):
    def test_migrators__quantity(self):
        # Sould match the settings version
        self.assertEqual(len(migrators), SETTINGS_VERSION)

    def test_to_v1(self):
        # Should set first 4 relays active=True if active is not set
        settings = Mock(
            get = Mock(return_value={"relay_pin": 17})
        )
        logger = Mock()
        to_v1(settings, logger)
        logger.info.assert_any_call("OctoRelay migrates to settings v1")
        for index in ["r1", "r2", "r3", "r4"]:
            settings.set.assert_any_call([index], {
                "relay_pin": 17,
                "active": True
            })

    def test_migrate(self):
        # Should call all migrations
        settings = Mock(
            get = Mock(return_value={})
        )
        logger = Mock()
        migrate(0, settings, logger)
        logger.info.assert_any_call("OctoRelay migrates to settings v1")


if __name__ == "__main__":
    unittest.main()
