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
from octoprint_octorelay.migrations import migrators
del sys.modules["octoprint_octorelay"] # avoid keeping __init__.py imported in this test

class TestMigrations(unittest.TestCase):
    def test_migrators__quantity(self):
        # Sould match the settings version
        self.assertEqual(len(migrators), SETTINGS_VERSION)

if __name__ == "__main__":
    unittest.main()
