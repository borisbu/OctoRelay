# -*- coding: utf-8 -*-
import unittest
from snapshottest import TestCase
from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("../octoprint_octorelay/templates/"))

class TestTemplates(TestCase):
    def test_templates(self):
        files = [
            "octorelay_settings.jinja2",
            "octorelay_navbar.jinja2"
        ]
        for file in files:
            template = environment.get_template(file)
            html = template.render({
                "_": lambda value: value
            })
            self.assertMatchSnapshot(html, file)

if __name__ == "__main__":
    unittest.main()
