# -*- coding: utf-8 -*-
import unittest
import sys
from unittest.mock import Mock
from snapshottest import TestCase
from jinja2 import Environment, FileSystemLoader

# Mocking required before the further import
sys.modules["RPi.GPIO"] = Mock()

# pylint: disable=wrong-import-position
from octoprint_octorelay.const import get_ui_vars

# avoid keeping other modules automatically imported by this test
if "octoprint_octorelay" in sys.modules:
    del sys.modules["octoprint_octorelay"]

environment = Environment(loader=FileSystemLoader("../octoprint_octorelay/templates/"))

class TestTemplates(TestCase):
    def test_templates(self):
        files = [
            "octorelay_settings.jinja2",
            "octorelay_navbar.jinja2"
        ]
        ui_vars = get_ui_vars()
        for file in files:
            template = environment.get_template(file)
            html = template.render({
                "_": lambda value: value,
                **{ "plugin_octorelay_" + key: value for key, value in ui_vars.items() }
            })
            self.assertMatchSnapshot(html, file)

if __name__ == "__main__":
    unittest.main()
