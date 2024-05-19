# -*- coding: utf-8 -*-
import unittest
import sys
from unittest.mock import Mock

# Mocks used for assertions
gpiod_mock = Mock()
line_mock = Mock()
gpiod_mock.request_lines = Mock(return_value=line_mock)
gpiod_mock.LineSettings = Mock(return_value="LineSettingsMock")
gpiod_mock.line = {
    "Direction": {
        "OUTPUT": "OutputMock"
    },
    "Value": {
        "ACTIVE": "ActiveMock",
        "INACTIVE": "InactiveMock"
    }
}
sys.modules["gpiod"] = gpiod_mock

# pylint: disable=wrong-import-position
from octoprint_octorelay.driver import Relay

# avoid keeping other modules automatically imported by this test
del sys.modules["octoprint_octorelay"]
del sys.modules["octoprint_octorelay.migrations"]
del sys.modules["octoprint_octorelay.task"]

class TestRelayDriver(unittest.TestCase):
    def test_constructor(self):
        relay = Relay(18, True)
        self.assertIsInstance(relay, Relay)
        self.assertEqual(relay.pin, 18)
        self.assertTrue(relay.inverted)

    def test_serialization(self):
        relay = Relay(18, True)
        serialization = f"{relay}"
        self.assertEqual(serialization, "Relay(pin=18,inverted=True,closed=True)")

    def test_close(self):
        cases = [
            { "relay": Relay(18, False), "expected_pin_state": True },
            { "relay": Relay(18, True), "expected_pin_state": False }
        ]
        for case in cases:
            case["relay"].close()
            gpiod_mock.LineSettings.assert_called_with(direction="OutputMock")
            gpiod_mock.request_lines.assert_called_with(
                "/dev/gpiochip0",
                consumer = "OctoRelay"
                config = { 18: "LineSettingsMock" }
            )
            lineMock.set_value.assert_called_with(18, case["expected_pin_state"])

    def test_open(self):
        cases = [
            { "relay": Relay(18, False), "expected_pin_state": False },
            { "relay": Relay(18, True), "expected_pin_state": True }
        ]
        for case in cases:
            case["relay"].open()
            gpiod_mock.LineSettings.assert_called_with(direction="OutputMock")
            gpiod_mock.request_lines.assert_called_with(
                "/dev/gpiochip0",
                consumer = "OctoRelay"
                config = { 18: "LineSettingsMock" }
            )
            lineMock.set_value.assert_called_with(18, case["expected_pin_state"])

    def test_is_closed(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_relay_state": True },
            { "mocked_state": 0, "inverted": False, "expected_relay_state": False },
            { "mocked_state": 1, "inverted": True, "expected_relay_state": False },
            { "mocked_state": 0, "inverted": True, "expected_relay_state": True },
        ]
        for case in cases:
            gpiod_mock.input = Mock(return_value=case["mocked_state"])
            relay = Relay(18, case["inverted"])
            self.assertEqual(relay.is_closed(), case["expected_relay_state"])
            gpiod_mock.setwarnings.assert_any_call(False)
            gpiod_mock.setwarnings.assert_called_with(True)
            gpiod_mock.input.assert_called_with(18)

    def test_toggle__no_argument(self):
        cases = [
            { "mocked_state": 1, "inverted": False, "expected_pin_state": False, "expected_relay_state": False },
            { "mocked_state": 0, "inverted": False, "expected_pin_state": True, "expected_relay_state": True },
            { "mocked_state": 1, "inverted": True, "expected_pin_state": False, "expected_relay_state": True },
            { "mocked_state": 0, "inverted": True, "expected_pin_state": True, "expected_relay_state": False },
        ]
        for case in cases:
            gpiod_mock.input = Mock(return_value=case["mocked_state"])
            relay = Relay(18, case["inverted"])
            self.assertEqual(relay.toggle(), case["expected_relay_state"])
            gpiod_mock.setwarnings.assert_any_call(False)
            gpiod_mock.setwarnings.assert_called_with(True)
            gpiod_mock.input.assert_called_with(18)
            gpiod_mock.setup.assert_called_with(18, "MockedOUT")
            gpiod_mock.output.assert_called_with(18, case["expected_pin_state"])

if __name__ == "__main__":
    unittest.main()
