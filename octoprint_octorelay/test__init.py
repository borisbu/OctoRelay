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

    def test_get_settings_defaults(self):
        expected = dict(
            r1=dict(
               active=True,
               relay_pin=4,
               inverted_output=True,
               initial_value=False,
               cmdON="",
               cmdOFF="",
               iconOn="&#128161;",
               iconOff="<div style=\"filter: grayscale(90%)\">&#128161;</div>",
               labelText="Light",
               confirmOff=False,
               autoONforPrint=True,
               autoOFFforPrint=True,
               autoOffDelay=10,
            ),
            r2=dict(
               active=True,
               relay_pin=17,
               inverted_output=True,
               initial_value=False,
               cmdON="",
               cmdOFF="",
               iconOn="""<img width="24" height="24" src="/plugin/octorelay/static/img/3d-printer.svg">""",
               iconOff="""<img width="24" height="24" src="/plugin/octorelay/static/img/3d-printer.svg" style="filter: opacity(20%)">""",
               labelText="Printer",
               confirmOff=True,
               autoONforPrint=False,
               autoOFFforPrint=False,
               autoOffDelay=0,
            ),
            r3=dict(
               active=True,
               relay_pin=18,
               inverted_output=True,
               initial_value=False,
               cmdON="",
               cmdOFF="",
               iconOn="""<img width="24" height="24" src="/plugin/octorelay/static/img/fan.svg" >""",
               iconOff="""<img width="24" height="24" src="/plugin/octorelay/static/img/fan.svg" style="filter: opacity(20%)">""",
               labelText="Fan",
               confirmOff=False,
               autoONforPrint=True,
               autoOFFforPrint=True,
               autoOffDelay=10,
            ),
            r4=dict(
               active = True,
               relay_pin=23,
               inverted_output=True,
               initial_value=True,
               cmdON="sudo service webcamd start",
               cmdOFF="sudo service webcamd stop",
               iconOn="""<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" >""",
               iconOff="""<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" style="filter: opacity(20%)">""",
               labelText="Webcam",
               confirmOff=False,
               autoONforPrint=True,
               autoOFFforPrint=True,
               autoOffDelay=10,
            ),
            r5=dict(
               active=False,
               relay_pin=24,
               inverted_output=True,
               initial_value=False,
               cmdON="",
               cmdOFF="",
               iconOn="ON",
               iconOff="OFF",
               labelText="R5",
               confirmOff=False,
               autoONforPrint=False,
               autoOFFforPrint=False,
               autoOffDelay=0,
            ),
            r6=dict(
               active=False,
               relay_pin=25,
               inverted_output=True,
               initial_value=False,
               cmdON="",
               cmdOFF="",
               iconOn="&#128161;",
               iconOff="<div style=\"filter: grayscale(90%)\">&#128161;</div>",
               labelText="R6",
               confirmOff=False,
               autoONforPrint=False,
               autoOFFforPrint=False,
               autoOffDelay=0,
            ),
            r7=dict(
               active=False,
               relay_pin=8,
               inverted_output=True,
               initial_value=False,
               cmdON="",
               cmdOFF="",
               iconOn="&#128161;",
               iconOff="<div style=\"filter: grayscale(90%)\">&#128161;</div>",
               labelText="R7",
               confirmOff=False,
               autoONforPrint=False,
               autoOFFforPrint=False,
               autoOffDelay=0,
            ),
            r8=dict(
               active=False,
               relay_pin=7,
               inverted_output=True,
               initial_value=False,
               cmdON="",
               cmdOFF="",
               iconOn="&#128161;",
               iconOff="<div style=\"filter: grayscale(90%)\">&#128161;</div>",
               labelText="R8",
               confirmOff=False,
               autoONforPrint=False,
               autoOFFforPrint=False,
               autoOffDelay=0,
            ),
        )
        actual = self.plugin_instance.get_settings_defaults()
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
