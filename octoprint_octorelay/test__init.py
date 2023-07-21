import unittest
from unittest.mock import Mock, patch, MagicMock
import os

# Patch RPi.GPIO module before importing OctoRelayPlugin class
RPi_mock = Mock()
sys.modules['RPi'] = RPi_mock
sys.modules['RPi.GPIO'] = RPi_mock

from __init__ import OctoRelayPlugin

class TestOctoRelayPlugin(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
