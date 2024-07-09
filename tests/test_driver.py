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
    def test_constructor(self):
        relay = Relay(18, True, MockFactory())
        self.assertIsInstance(relay, Relay)
        self.assertEqual(relay.pin, 18)
        self.assertTrue(relay.inverted)

    def test_serialization(self):
        relay = Relay(18, True, MockFactory())
        serialization = f"{relay}"
        self.assertEqual(serialization, "Relay(pin=18,inverted=True,closed=True)")

    def test_close(self):
        cases = [
            { "relay": Relay(18, False, MockFactory()), "expected_pin_state": True },
            { "relay": Relay(18, True, MockFactory()), "expected_pin_state": False }
        ]
        for case in cases:
            case["relay"].close()
            self.assertEqual(case["relay"].relay.is_lit, case["expected_pin_state"])

    def test_open(self):
        cases = [
            { "relay": Relay(18, False, MockFactory()), "expected_pin_state": False },
            { "relay": Relay(18, True, MockFactory()), "expected_pin_state": True }
        ]
        for case in cases:
            case["relay"].open()
            self.assertEqual(case["relay"].relay.is_lit, case["expected_pin_state"])

    def test_is_closed(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_relay_state": True },
            { "mocked_state": 0, "inverted": False, "expected_relay_state": False },
            { "mocked_state": 1, "inverted": True, "expected_relay_state": False },
            { "mocked_state": 0, "inverted": True, "expected_relay_state": True },
        ]
        for case in cases:
            relay = Relay(18, case["inverted"], MockFactory())
            relay.relay.value = case["mocked_state"]
            self.assertEqual(relay.is_closed(), case["expected_relay_state"])

    def test_toggle__no_argument(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_pin_state": False, "expected_relay_state": False },
            { "mocked_state": 0, "inverted": False, "expected_pin_state": True, "expected_relay_state": True },
            { "mocked_state": 1, "inverted": True, "expected_pin_state": False, "expected_relay_state": True },
            { "mocked_state": 0, "inverted": True, "expected_pin_state": True, "expected_relay_state": False },
        ]
        for case in cases:
            relay = Relay(18, case["inverted"], MockFactory())
            relay.relay.value = case["mocked_state"]
            self.assertEqual(relay.toggle(), case["expected_relay_state"])
            self.assertEqual(relay.relay.is_lit, case["expected_pin_state"])

if __name__ == "__main__":
    unittest.main()
