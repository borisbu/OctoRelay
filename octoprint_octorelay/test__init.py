import unittest
import sys
from unittest.mock import Mock, patch, MagicMock
import os

# Patch RPi.GPIO module before importing OctoRelayPlugin class
RPi_mock = Mock()
sys.modules['RPi'] = RPi_mock
sys.modules['RPi.GPIO'] = RPi_mock

from __init__ import OctoRelayPlugin

class TestOctoRelayPlugin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create an instance of the OctoRelayPlugin class
        cls.plugin_instance = octorelay.OctoRelayPlugin()

    @classmethod
    def tearDownClass(cls):
        # Clean up
        del sys.modules['RPi']
        del sys.modules['RPi.GPIO']

if __name__ == '__main__':
    unittest.main()
