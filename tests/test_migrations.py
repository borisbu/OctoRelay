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
from octoprint_octorelay.migrations import migrators, migrate, v0

# avoid keeping other modules automatically imported by this test
del sys.modules["octoprint_octorelay"]
del sys.modules["octoprint_octorelay.driver"]

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
