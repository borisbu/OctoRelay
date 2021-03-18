# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
from octoprint.events import Events
import flask
import asyncio

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
				confirmOff = False,
				autoONforPrint = True,
				autoOFFforPrint = True,
				autoOffDelay = 10,
			),
			r2=dict(
				active = True,
				relay_pin = 17,
				inverted_output = True,
				initial_value = False,
				iconOn = """<img src="/plugin/octorelay/static/img/3d-printer.png" highth="24" width="24">""",
				iconOff = """<img src="/plugin/octorelay/static/img/3d-printer.png" highth="24" width="24" style="filter: opacity(20%)">""",
				labelText = "Printer",
				confirmOff = True,
				autoONforPrint = False,
				autoOFFforPrint = False,
				autoOffDelay = 0,
			),
			r3=dict(
				active = True,
				relay_pin = 18,
				inverted_output = True,
				initial_value = False,
				iconOn = """<img highth="24" width="24" src="/plugin/octorelay/static/img/fan-24.png" >""",
				iconOff = """<img highth="24" width="24" src="/plugin/octorelay/static/img/fan-24.png" style="filter: opacity(20%)">""",
				labelText = "Fan",
				confirmOff = False,
				autoONforPrint = True,
				autoOFFforPrint = True,
				autoOffDelay = 10,
			),
			r4=dict(
				active = True,
				relay_pin = 23,
				inverted_output = True,
				initial_value = False,
				iconOn = "&#127765;",
				iconOff = "&#127761;",
				labelText = "R4",
				confirmOff = False,
				autoONforPrint = False,
				autoOFFforPrint = False,
				autoOffDelay = 0,
			),
			r5=dict(
				active = False,
				relay_pin = 24,
				inverted_output = True,
				initial_value = False,
				iconOn = "ON",
				iconOff = "OFF",
				labelText = "R5",
				confirmOff = False,
				autoONforPrint = False,
				autoOFFforPrint = False,
				autoOffDelay = 0,
			),
			r6=dict(
				active = False,
				relay_pin = 25,
				inverted_output = True,
				initial_value = False,
				iconOn = "&#128161;",
				iconOff = "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
				labelText = "R6",
				confirmOff = False,
				autoONforPrint = False,
				autoOFFforPrint = False,
				autoOffDelay = 0,
			),
			r7=dict(
				active = False,
				relay_pin = 8,
				inverted_output = True,
				initial_value = False,
				iconOn = "&#128161;",
				iconOff = "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
				labelText = "R7",
				confirmOff = False,
				autoONforPrint = False,
				autoOFFforPrint = False,
				autoOffDelay = 0,
			),
			r8=dict(
				active = False,
				relay_pin = 7,
				inverted_output = True,
				initial_value = False,
				iconOn = "&#128161;",
				iconOff = "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
				labelText = "R8",
				confirmOff = False,
				autoONforPrint = False,
				autoOFFforPrint = False,
				autoOffDelay = 0,
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
		elif event == Events.PRINT_STARTED:
			self._logger.debug("Got event: {}".format(event))
			self.print_started()
		elif event == Events.PRINT_DONE:
			self._logger.debug("Got event: {}".format(event))
			self.print_stopped()
		elif event == Events.PRINT_FAILED:
			self._logger.debug("Got event: {}".format(event))
			self.print_stopped()
		elif event == Events.PRINT_CANCELLING:
			self._logger.debug("Got event: {}".format(event))
			self.print_stopped()
		elif event == Events.PRINT_CANCELLED:
			self._logger.debug("Got event: {}".format(event))
			self.print_stopped()
		return

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		self.update_ui()

	def print_started(self):
		for n in range(1,9):
			index = "r"+str(n)
			settings = self.get_settings_defaults()[index]
			settings.update(self._settings.get([index]))

			autoONforPrint = settings['autoONforPrint']
			if autoONforPrint:
				relay_pin = int(settings["relay_pin"])
				inverted = settings['inverted_output']

				GPIO.setwarnings(False)
				GPIO.setup(relay_pin,GPIO.OUT)
				# XOR with inverted
				GPIO.output(relay_pin, inverted != True)
				GPIO.setwarnings(True)
		self.update_ui()

	def print_stopped(self):
		for n in range(1,9):
			index = "r"+str(n)
			settings = self.get_settings_defaults()[index]
			settings.update(self._settings.get([index]))

			relay_pin = int(settings["relay_pin"])
			inverted = settings['inverted_output']
			autoOFFforPrint = settings['autoOFFforPrint']
			autoOffDelay = int(settings['autoOffDelay'])
			if autoOFFforPrint:
				self._logger.debug("turn off pin: {} in {} seconds. index: {}".format(relay_pin, autoOffDelay, index))
				asyncio.run(self.turn_off_pin(autoOffDelay,relay_pin,inverted))
		self.update_ui()


	async def turn_off_pin(self, delay, relay_pin, inverted):
		self._logger.info("turn off pin: {} in {} seconds.".format(relay_pin, delay))
		await asyncio.sleep(delay)
		GPIO.setwarnings(False)
		GPIO.setup(relay_pin, GPIO.OUT)
		# XOR with inverted
		GPIO.output(relay_pin, inverted != False)
		GPIO.setwarnings(True)
		self._logger.info("pin: {} turned off".format(relay_pin))
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
			confirmOff = settings['confirmOff']

			# set the icon state
			GPIO.setwarnings(False)
			GPIO.setup(relay_pin, GPIO.OUT)
			ledState = inverted != GPIO.input(relay_pin)
			GPIO.setwarnings(True)
			if ledState:
				self.model[index]['iconText'] = iconOn
				self.model[index]['confirmOff'] = confirmOff
			else:
				self.model[index]['iconText'] = iconOff
				self.model[index]['confirmOff'] = False
			self.model[index]['labelText'] = labelText
			self.model[index]['active'] = active

		#self._logger.info("update ui with model {}".format(self.model))
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
