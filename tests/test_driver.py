# -*- coding: utf-8 -*-
import unittest
import sys

from gpiozero.pins.mock import MockFactory

# pylint: disable=wrong-import-position
from octoprint_octorelay.driver import Driver

# avoid keeping other modules automatically imported by this test
del sys.modules["octoprint_octorelay"]
del sys.modules["octoprint_octorelay.migrations"]
del sys.modules["octoprint_octorelay.task"]

class TestDriver(unittest.TestCase):
    def test_constructor(self):
        relay = Driver(18, True, MockFactory())
        self.assertIsInstance(relay, Driver)
        self.assertEqual(relay.pin, 18)
        self.assertTrue(relay.inverted)

    def test_serialization(self):
        relay = Driver(18, True, MockFactory())
        serialization = f"{relay}"
        self.assertEqual(serialization, "Driver(pin=18,inverted=True,closed=False)")

    def test_close(self):
        cases = [
            { "relay": Driver(18, False, MockFactory()), "expected_pin_state": True },
            { "relay": Driver(18, True, MockFactory()), "expected_pin_state": False }
        ]
        for case in cases:
            case["relay"].close()
            self.assertEqual(case["relay"].handle.is_lit, case["expected_pin_state"])

    def test_open(self):
        cases = [
            { "relay": Driver(18, False, MockFactory()), "expected_pin_state": False },
            { "relay": Driver(18, True, MockFactory()), "expected_pin_state": True }
        ]
        for case in cases:
            case["relay"].open()
            self.assertEqual(case["relay"].handle.is_lit, case["expected_pin_state"])

    def test_is_closed(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_relay_state": True },
            { "mocked_state": 0, "inverted": False, "expected_relay_state": False },
            { "mocked_state": 1, "inverted": True, "expected_relay_state": False },
            { "mocked_state": 0, "inverted": True, "expected_relay_state": True },
        ]
        for case in cases:
            relay = Driver(18, case["inverted"], MockFactory())
            relay.handle.value = case["mocked_state"]
            self.assertEqual(relay.is_closed(), case["expected_relay_state"])

    def test_toggle__no_argument(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_pin_state": False, "expected_relay_state": False },
            { "mocked_state": 0, "inverted": False, "expected_pin_state": True, "expected_relay_state": True },
            { "mocked_state": 1, "inverted": True, "expected_pin_state": False, "expected_relay_state": True },
            { "mocked_state": 0, "inverted": True, "expected_pin_state": True, "expected_relay_state": False },
        ]
        for case in cases:
            relay = Driver(18, case["inverted"], MockFactory())
            relay.handle.value = case["mocked_state"]
            self.assertEqual(relay.toggle(), case["expected_relay_state"])
            self.assertEqual(relay.handle.is_lit, case["expected_pin_state"])

    def test_ensure(self):
        # Test creating a new relay
        relay1 = Driver.ensure(17, False, MockFactory())
        self.assertEqual(len(Driver.cache), 1)
        self.assertEqual(relay1.pin, 17)
        self.assertFalse(relay1.inverted)

        # Test retrieving the existing relay with the same pin and inversion
        relay2 = Driver.ensure(17, True, MockFactory())
        self.assertIs(relay1, relay2)
        self.assertEqual(len(Driver.cache), 1)  # Should still be 1

        # Test retrieving the existing relay with the same pin but different inversion
        relay3 = Driver.ensure(17, True, MockFactory())
        self.assertEqual(len(Driver.cache), 1)  # Should still be 1
        self.assertIs(relay1, relay3)
        self.assertTrue(relay1.inverted)  # Inversion should be updated

    def tearDown(self):
        # Clear cache after each test
        Driver.cache = []

if __name__ == "__main__":
    unittest.main()
