# -*- coding: utf-8 -*-
import unittest
import sys
from unittest.mock import Mock

# Mocks used for assertions
gpiod_mock = Mock()
line_mock = Mock()
gpiod_mock.request_lines = Mock(return_value=line_mock)
gpiod_mock.LineSettings = Mock(return_value="LineSettingsMock")
sys.modules["gpiod"] = gpiod_mock
line_mock.Direction = Mock()
line_mock.Direction.OUTPUT = "OutputMock"
line_mock.Value = Mock()
line_mock.Value.ACTIVE = "ActiveMock"
line_mock.Value.INACTIVE = "InactiveMock"
sys.modules["gpiod.line"] = line_mock

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
            { "relay": Relay(18, False), "expected_pin_state": "ActiveMock" },
            { "relay": Relay(18, True), "expected_pin_state": "InactiveMock" }
        ]
        for case in cases:
            case["relay"].close()
            gpiod_mock.LineSettings.assert_called_with(direction="OutputMock")
            gpiod_mock.request_lines.assert_called_with(
                "/dev/gpiochip0",
                consumer = "OctoRelay",
                config = { 18: "LineSettingsMock" }
            )
            line_mock.set_value.assert_called_with(18, case["expected_pin_state"])

    def test_open(self):
        cases = [
            { "relay": Relay(18, False), "expected_pin_state": "InactiveMock" },
            { "relay": Relay(18, True), "expected_pin_state": "ActiveMock" }
        ]
        for case in cases:
            case["relay"].open()
            gpiod_mock.LineSettings.assert_called_with(direction="OutputMock")
            gpiod_mock.request_lines.assert_called_with(
                "/dev/gpiochip0",
                consumer = "OctoRelay",
                config = { 18: "LineSettingsMock" }
            )
            line_mock.set_value.assert_called_with(18, case["expected_pin_state"])

    def test_is_closed(self):
        cases = [
            { "mocked_state": "ActiveMock", "inverted": False, "expected_relay_state": True },
            { "mocked_state": "InactiveMock", "inverted": False, "expected_relay_state": False },
            { "mocked_state": "ActiveMock", "inverted": True, "expected_relay_state": False },
            { "mocked_state": "InactiveMock", "inverted": True, "expected_relay_state": True },
        ]
        for case in cases:
            line_mock.get_value = Mock(return_value=case["mocked_state"])
            relay = Relay(18, case["inverted"])
            self.assertEqual(relay.is_closed(), case["expected_relay_state"])
            line_mock.get_value.assert_called_with(18)

    def test_toggle__no_argument(self):
        cases = [
            { "mocked_state": "ActiveMock", "inverted": False, "expected_pin_state": False, "expected_relay_state": False },
            { "mocked_state": "InactiveMock", "inverted": False, "expected_pin_state": True, "expected_relay_state": True },
            { "mocked_state": "ActiveMock", "inverted": True, "expected_pin_state": False, "expected_relay_state": True },
            { "mocked_state": "InactiveMock", "inverted": True, "expected_pin_state": True, "expected_relay_state": False },
        ]
        for case in cases:
            line_mock.get_value = Mock(return_value=case["mocked_state"])
            relay = Relay(18, case["inverted"])
            self.assertEqual(relay.toggle(), case["expected_relay_state"])
            line_mock.get_value.assert_called_with(18)
            gpiod_mock.LineSettings.assert_called_with(direction="OutputMock")
            gpiod_mock.request_lines.assert_called_with(
                "/dev/gpiochip0",
                consumer = "OctoRelay",
                config = { 18: "LineSettingsMock" }
            )
            line_mock.set_value.assert_called_with(18, "ActiveMock" if case["expected_pin_state"] else "InactiveMock")

if __name__ == "__main__":
    unittest.main()
