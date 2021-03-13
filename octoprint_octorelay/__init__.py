# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
from octoprint.events import Events
import flask

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class OctoRelayPlugin(
		octoprint.plugin.AssetPlugin,
		octoprint.plugin.StartupPlugin,
		octoprint.plugin.TemplatePlugin,
		octoprint.plugin.SimpleApiPlugin,
		octoprint.plugin.SettingsPlugin,
		octoprint.plugin.EventHandlerPlugin,
		octoprint.plugin.RestartNeedingPlugin
	):

	def get_settings_defaults(self):
		return dict(
			r1=dict(
				active = True,
				relay_pin = 4,
				inverted_output = True,
				initial_value = False,
				iconOn = "&#128161;",
				iconOff = "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
				labelText = "Light",
			),
			r2=dict(
				active = True,
				relay_pin = 17,
				inverted_output = True,
				initial_value = False,
				iconOn = """<img src="https://github.com/borisbu/OctoRelay/blob/master/img/3d-printer.png?raw=true" highth="24" width="24">""",
				iconOff = """<img src="https://github.com/borisbu/OctoRelay/blob/master/img/3d-printer.png?raw=true" highth="24" width="24" style="filter: opacity(20%)">""",
				labelText = "Printer",
			),
			r3=dict(
				active = True,
				relay_pin = 18,
				inverted_output = True,
				initial_value = False,
				iconOn = """<img highth="24" width="24" src="https://github.com/borisbu/OctoRelay/blob/master/img/fan-24.png?raw=true" >""",
				iconOff = """<img highth="24" width="24" src="https://github.com/borisbu/OctoRelay/blob/master/img/fan-24.png?raw=true" style="filter: opacity(20%)">""",
				labelText = "Fan",
			),
			r4=dict(
				active = True,
				relay_pin = 23,
				inverted_output = True,
				initial_value = False,
				iconOn = "&#127765;",
				iconOff = "&#127761;",
				labelText = "R4",
			),
			r5=dict(
				active = False,
				relay_pin = 24,
				inverted_output = True,
				initial_value = False,
				iconOn = "ON",
				iconOff = "OFF",
				labelText = "R5",
			),
			r6=dict(
				active = False,
				relay_pin = 25,
				inverted_output = True,
				initial_value = False,
				iconOn = "&#128161;",
				iconOff = "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
				labelText = "R6",
			),
			r7=dict(
				active = False,
				relay_pin = 8,
				inverted_output = True,
				initial_value = False,
				iconOn = "&#128161;",
				iconOff = "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
				labelText = "R7",
			),
			r8=dict(
				active = False,
				relay_pin = 7,
				inverted_output = True,
				initial_value = False,
				iconOn = "&#128161;",
				iconOff = "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
				labelText = "R8",
			),
		)

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/octorelay.js"],
		)

	def on_after_startup(self):

		self._logger.info("--------------------------------------------")
		self._logger.info("start OctoRelay")

		self.model = dict()
		for n in range(1,9):
			index = "r"+str(n)
			self.model[index] = dict()

			settings = self.get_settings_defaults()[index]
			settings.update(self._settings.get([index]))
			self._logger.debug("settings for {}: {}".format(index, settings))

			active = int(settings["active"])
			if (active):
				relay_pin = int(settings["relay_pin"])
				initial_value = settings['initial_value']
				inverted = settings['inverted_output']

				# Setting the default state of pin
				GPIO.setwarnings(False)
				GPIO.setup(relay_pin,GPIO.OUT)
				# XOR with inverted
				GPIO.output(relay_pin, initial_value != inverted)
				GPIO.setwarnings(True)

		self.update_ui()

		self._logger.info("OctoRelay plugin started")
		self._logger.info("--------------------------------------------")

	def get_api_commands(self):
		return {
			"update": [],
		}

	def on_api_command(self, command, data):
		self._logger.debug("on_api_command {}, some_parameter is {}".format(command,data))
		index = data['pin']

		settings = self.get_settings_defaults()[index]
		settings.update(self._settings.get([index]))

		relay_pin = int(settings["relay_pin"])
		inverted = settings['inverted_output']

		GPIO.setwarnings(False)

		GPIO.setup(relay_pin, GPIO.OUT)
		# XOR with inverted
		ledState = inverted != GPIO.input(relay_pin)

		self._logger.debug("Ocotrelay before pin: {}, inverted: {}, currentState: {}".format(
			relay_pin,
			inverted,
			ledState
		))

		#toggle state
		ledState = not ledState

		GPIO.setup(relay_pin,GPIO.OUT)
		# XOR with inverted
		GPIO.output(relay_pin, inverted != ledState)

		GPIO.setwarnings(True)

		self.update_ui()

		return flask.jsonify(status="ok")

	def on_event(self, event, payload):
		if event == Events.CLIENT_OPENED:
			self.update_ui()
		return

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		self.update_ui()

	def update_ui(self):
		for n in range(1,9):
			index = "r"+str(n)
			settings = self.get_settings_defaults()[index]
			settings.update(self._settings.get([index]))

			labelText = settings["labelText"]
			active = int(settings["active"])
			relay_pin = int(settings["relay_pin"])
			inverted = settings['inverted_output']
			iconOn = settings['iconOn']
			iconOff = settings['iconOff']

			# set the icon state
			GPIO.setwarnings(False)
			GPIO.setup(relay_pin, GPIO.OUT)
			ledState = inverted != GPIO.input(relay_pin)
			GPIO.setwarnings(True)
			if ledState:
				self.model[index]['iconText'] = iconOn
			else:
				self.model[index]['iconText'] = iconOff
			self.model[index]['labelText'] = labelText
			self.model[index]['active'] = active

		self._plugin_manager.send_plugin_message(self._identifier, self.model)


	def get_update_information(self):
		return dict(
			octorelay=dict(
				displayName="OctoRelay",
				displayVersion=self._plugin_version,

				type="github_release",
				current=self._plugin_version,

				user="borisbu",
				repo="OctoRelay",
				pip="https://github.com/borisbu/OctoRelay/archive/{target}.zip"
			)
		)
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = OctoRelayPlugin()

__plugin_hooks__ = {
	"octoprint.plugin.softwareupdate.check_config":
	__plugin_implementation__.get_update_information
}
