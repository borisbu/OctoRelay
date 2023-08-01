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
        relay = Relay(18, False)
        self.assertIsInstance(relay, Relay)
