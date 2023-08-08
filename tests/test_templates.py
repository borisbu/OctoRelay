# -*- coding: utf-8 -*-
import unittest
from snapshottest import TestCase
from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("../octoprint_octorelay/templates/"))

class TestTemplates(TestCase):
    def test_settings(self):
        template = environment.get_template("octorelay_settings.jinja2")
        html = template.render({
            "_": lambda value: value
        })
        self.assertMatchSnapshot(html, "settings")

if __name__ == "__main__":
    unittest.main()
