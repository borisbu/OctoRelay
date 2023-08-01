# -*- coding: utf-8 -*-
import unittest
import sys
from unittest.mock import Mock

GPIO_mock = sys.modules["RPi.GPIO"] # mocked in test__init.py

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
            GPIO_mock.setup.assert_called_with(18, "MockedOUT")
            GPIO_mock.output.assert_called_with(18, case["expected_pin_state"])
            GPIO_mock.setwarnings.assert_any_call(False)
            GPIO_mock.setwarnings.assert_called_with(True)

    def test_open(self):
        cases = [
            { "relay": Relay(18, False), "expected_pin_state": False },
            { "relay": Relay(18, True), "expected_pin_state": True }
        ]
        for case in cases:
            case["relay"].open()
            GPIO_mock.setup.assert_called_with(18, "MockedOUT")
            GPIO_mock.output.assert_called_with(18, case["expected_pin_state"])
            GPIO_mock.setwarnings.assert_any_call(False)
            GPIO_mock.setwarnings.assert_called_with(True)

    def test_get_pin_state(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_pin_state": True },
            { "mocked_state": 0, "inverted": False, "expected_pin_state": False },
            { "mocked_state": 1, "inverted": True, "expected_pin_state": True },
            { "mocked_state": 0, "inverted": True, "expected_pin_state": False },
        ]
        for case in cases:
            GPIO_mock.input = Mock(return_value=case["mocked_state"])
            relay = Relay(18, case["inverted"])
            self.assertEqual(relay.get_pin_state(), case["expected_pin_state"])
            GPIO_mock.setwarnings.assert_any_call(False)
            GPIO_mock.setwarnings.assert_called_with(True)
            GPIO_mock.input.assert_called_with(18)

    def test_is_closed(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_relay_state": True },
            { "mocked_state": 0, "inverted": False, "expected_relay_state": False },
            { "mocked_state": 1, "inverted": True, "expected_relay_state": False },
            { "mocked_state": 0, "inverted": True, "expected_relay_state": True },
        ]
        for case in cases:
            GPIO_mock.input = Mock(return_value=case["mocked_state"])
            relay = Relay(18, case["inverted"])
            self.assertEqual(relay.is_closed(), case["expected_relay_state"])
            GPIO_mock.setwarnings.assert_any_call(False)
            GPIO_mock.setwarnings.assert_called_with(True)
            GPIO_mock.input.assert_called_with(18)

    def test_toggle__no_argument(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_pin_state": False, "expected_relay_state": False },
            { "mocked_state": 0, "inverted": False, "expected_pin_state": True, "expected_relay_state": True },
            { "mocked_state": 1, "inverted": True, "expected_pin_state": False, "expected_relay_state": True },
            { "mocked_state": 0, "inverted": True, "expected_pin_state": True, "expected_relay_state": False },
        ]
        for case in cases:
            GPIO_mock.input = Mock(return_value=case["mocked_state"])
            relay = Relay(18, case["inverted"])
            self.assertEqual(relay.toggle(), case["expected_relay_state"])
            GPIO_mock.setwarnings.assert_any_call(False)
            GPIO_mock.setwarnings.assert_called_with(True)
            GPIO_mock.input.assert_called_with(18)
            GPIO_mock.setup.assert_called_with(18, "MockedOUT")
            GPIO_mock.output.assert_called_with(18, case["expected_pin_state"])
