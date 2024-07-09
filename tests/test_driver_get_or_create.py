# -*- coding: utf-8 -*-
import unittest
import sys
from unittest.mock import Mock

from gpiozero.pins.mock import MockFactory

# pylint: disable=wrong-import-position
from octoprint_octorelay.driver import Relay

# avoid keeping other modules automatically imported by this test
del sys.modules["octoprint_octorelay"]
del sys.modules["octoprint_octorelay.migrations"]
del sys.modules["octoprint_octorelay.task"]

class TestRelayDriver(unittest.TestCase):
    def test_get(self):
        relay1 = Relay.get_or_create_relay(20, False, MockFactory())
        relay2 = Relay.get_or_create_relay(20, False, MockFactory())
        
        self.assertIs(relay1, relay2)
        self.assertEqual(len(Relay.relays), 1)
        
        relay3 = Relay.get_or_create_relay(21, True, MockFactory())
        self.assertNotEqual(relay1, relay3)
        self.assertEqual(len(Relay.relays), 2)

    def test_get_or_create_relay(self):
        # Test creating a new relay
        relay1 = Relay.get_or_create_relay(17, False, MockFactory())
        self.assertEqual(len(Relay.relays), 1)
        self.assertEqual(relay1.pin, 17)
        self.assertFalse(relay1.inverted)
    
        # Test retrieving the existing relay with the same pin and inversion
        relay2 = Relay.get_or_create_relay(17, False, MockFactory())
        self.assertEqual(len(Relay.relays), 1)  # Should still be 1

        # Test retrieving the existing relay with the same pin but different inversion
        relay3 = Relay.get_or_create_relay(17, True, MockFactory())
        self.assertEqual(len(Relay.relays), 1)  # Should still be 1
        self.assertIs(relay1, relay3)
        self.assertTrue(relay1.inverted)  # Inversion should be updated

    def tearDown(self):
        # Clear relays after each test
        Relay.relays = []

if __name__ == "__main__":
    unittest.main()
