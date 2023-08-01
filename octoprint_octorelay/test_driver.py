# -*- coding: utf-8 -*-
import unittest
import sys
from unittest.mock import Mock

class TestRelayDriver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.GPIO_mock = Mock()
        print(f"the correct mock {cls.GPIO_mock}")
        cls.GPIO_mock.OUT = "MockedOUT"
        sys.modules["RPi.GPIO"] = cls.GPIO_mock
        from octoprint_octorelay.driver import Relay
        def makeRelay(self, pin: int, inverted: bool):
            return Relay(pin, inverted)
        cls.makeRelay = makeRelay

    @classmethod
    def tearDownClass(cls):
        del sys.modules["RPi.GPIO"]

    def test_constructor(self):
        relay = self.makeRelay(18, True)
        self.assertEqual(relay.pin, 18)
        self.assertTrue(relay.inverted)

    def test_serialization(self):
        relay = self.makeRelay(18, True)
        serialization = f"{relay}"
        self.assertEqual(serialization, "Relay(pin=18,inverted=True)")

    def test_close(self):
        cases = [
            { "relay": self.makeRelay(18, False), "expected_pin_state": True },
            { "relay": self.makeRelay(18, True), "expected_pin_state": False }
        ]
        for case in cases:
            case["relay"].close()
            self.GPIO_mock.setup.assert_called_with(18, "MockedOUT")
            self.GPIO_mock.output.assert_called_with(18, case["expected_pin_state"])
            self.GPIO_mock.setwarnings.assert_any_call(False)
            self.GPIO_mock.setwarnings.assert_called_with(True)

    def test_open(self):
        cases = [
            { "relay": self.makeRelay(18, False), "expected_pin_state": False },
            { "relay": self.makeRelay(18, True), "expected_pin_state": True }
        ]
        for case in cases:
            case["relay"].open()
            self.GPIO_mock.setup.assert_called_with(18, "MockedOUT")
            self.GPIO_mock.output.assert_called_with(18, case["expected_pin_state"])
            self.GPIO_mock.setwarnings.assert_any_call(False)
            self.GPIO_mock.setwarnings.assert_called_with(True)

    def test_get_pin_state(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_pin_state": True },
            { "mocked_state": 0, "inverted": False, "expected_pin_state": False },
            { "mocked_state": 1, "inverted": True, "expected_pin_state": True },
            { "mocked_state": 0, "inverted": True, "expected_pin_state": False },
        ]
        for case in cases:
            self.GPIO_mock.input = Mock(return_value=case["mocked_state"])
            relay = self.makeRelay(18, case["inverted"])
            self.assertEqual(relay.get_pin_state(), case["expected_pin_state"])
            self.GPIO_mock.setwarnings.assert_any_call(False)
            self.GPIO_mock.setwarnings.assert_called_with(True)
            self.GPIO_mock.input.assert_called_with(18)

    def test_is_closed(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_relay_state": True },
            { "mocked_state": 0, "inverted": False, "expected_relay_state": False },
            { "mocked_state": 1, "inverted": True, "expected_relay_state": False },
            { "mocked_state": 0, "inverted": True, "expected_relay_state": True },
        ]
        for case in cases:
            self.GPIO_mock.input = Mock(return_value=case["mocked_state"])
            relay = self.makeRelay(18, case["inverted"])
            self.assertEqual(relay.is_closed(), case["expected_relay_state"])
            self.GPIO_mock.setwarnings.assert_any_call(False)
            self.GPIO_mock.setwarnings.assert_called_with(True)
            self.GPIO_mock.input.assert_called_with(18)

    def test_toggle__no_argument(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_pin_state": False, "expected_relay_state": False },
            { "mocked_state": 0, "inverted": False, "expected_pin_state": True, "expected_relay_state": True },
            { "mocked_state": 1, "inverted": True, "expected_pin_state": False, "expected_relay_state": True },
            { "mocked_state": 0, "inverted": True, "expected_pin_state": True, "expected_relay_state": False },
        ]
        for case in cases:
            self.GPIO_mock.input = Mock(return_value=case["mocked_state"])
            relay = self.makeRelay(18, case["inverted"])
            self.assertEqual(relay.toggle(), case["expected_relay_state"])
            self.GPIO_mock.setwarnings.assert_any_call(False)
            self.GPIO_mock.setwarnings.assert_called_with(True)
            self.GPIO_mock.input.assert_called_with(18)
            self.GPIO_mock.setup.assert_called_with(18, "MockedOUT")
            self.GPIO_mock.output.assert_called_with(18, case["expected_pin_state"])
