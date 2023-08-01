# -*- coding: utf-8 -*-
import unittest
import sys
from unittest.mock import Mock

GPIO_mock = Mock()
GPIO_mock.OUT = "MockedOUT"
sys.modules["RPi.GPIO"] = GPIO_mock

# pylint: disable=wrong-import-position
from octoprint_octorelay.driver import Relay

class TestRelayDriver(unittest.TestCase):
    def test_constructor(self):
        relay = Relay(18, True)
        self.assertIsInstance(relay, Relay)
        self.assertEqual(relay.pin, 18)
        self.assertTrue(relay.inverted)

    def test_serialization(self):
        relay = Relay(18, True)
        serialization = f"{relay}"
        self.assertEqual(serialization, "Relay(pin=18,inverted=True)")

    def test_close(self):
        cases = [
            { "relay": Relay(18, False), "expected_pin_state": True },
            { "relay": Relay(18, True), "expected_pin_state": False }
        ]
        for case in cases:
            case["relay"].close()
            GPIO_mock.setup.assert_called_with("MockedOUT")
            GPIO_mock.output.assert_called_with(18, case["expected_pin_state"])
            GPIO_mock.setwarnings.assert_any_call(False)
            GPIO_mock.setwarnings.assert_called_with(True)
