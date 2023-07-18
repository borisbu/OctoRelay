# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
from octoprint.events import Events
from octoprint.util import ResettableTimer
from octoprint.util import RepeatedTimer

import flask
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

POLLING_INTERVAL = 0.3


class OctoRelayPlugin(
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.ShutdownPlugin,
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.RestartNeedingPlugin
):

    def __init__(self):
        self.polling_timer = None
        self.model = None
        self.turn_off_timers = None

    def get_settings_defaults(self):
        return dict(
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
                iconOn="""<img src="/plugin/octorelay/static/img/3d-printer.png" highth="24" width="24">""",
                iconOff="""<img src="/plugin/octorelay/static/img/3d-printer.png" highth="24" width="24" style="filter: opacity(20%)">""",
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
                iconOn="""<img highth="24" width="24" src="/plugin/octorelay/static/img/fan-24.png" >""",
                iconOff="""<img highth="24" width="24" src="/plugin/octorelay/static/img/fan-24.png" style="filter: opacity(20%)">""",
                labelText="Fan",
                confirmOff=False,
                autoONforPrint=True,
                autoOFFforPrint=True,
                autoOffDelay=10,
            ),
            r4=dict(
                active=True,
                relay_pin=23,
                inverted_output=True,
                initial_value=True,
                cmdON="sudo service webcamd start",
                cmdOFF="sudo service webcamd stop",
                iconOn="""<img highth="24" width="24" src="/plugin/octorelay/static/img/webcam.png" >""",
                iconOff="""<img highth="24" width="24" src="/plugin/octorelay/static/img/webcam.png" style="filter: opacity(20%)">""",
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
        self.turn_off_timers = dict()

        settings = self.get_settings_defaults()

        for index in settings:
            settings[index].update(self._settings.get([index]))
            self._logger.debug("settings for {}: {}".format(index, settings[index]))

            self.model[index] = dict()
            if settings[index]['active']:
                relay_pin = int(settings[index]['relay_pin'])
                initial_value = settings[index]['initial_value']
                inverted_output = settings[index]['inverted_output']

                # Setting the default state of pin
                GPIO.setup(relay_pin, GPIO.OUT)
                # XOR with inverted
                GPIO.output(relay_pin, initial_value != inverted_output)

        self.update_ui()
        self.polling_timer = RepeatedTimer(POLLING_INTERVAL, self.input_polling, daemon=True)
        self.polling_timer.start()

        self._logger.info("OctoRelay plugin started")
        self._logger.info("--------------------------------------------")

    def on_shutdown(self):
        self.polling_timer.cancel()
        self._logger.info("OctoRelay plugin stopped")
        self._logger.info("--------------------------------------------")

    def update_relay(self, index, get_status=False):
        try:
            settings = self._settings.get([index], merged=True)

            relay_pin = int(settings["relay_pin"])
            inverted = settings['inverted_output']
            cmd_on = settings['cmdON']
            cmd_off = settings['cmdOFF']

            GPIO.setwarnings(False)

            GPIO.setup(relay_pin, GPIO.OUT)
            # XOR with inverted
            led_state = inverted != GPIO.input(relay_pin)

            if get_status:
                return led_state

            self._logger.debug("Ocotrelay before pin: {}, inverted: {}, currentState: {}".format(
                relay_pin,
                inverted,
                led_state
            ))

            # toggle state
            led_state = not led_state

            GPIO.setup(relay_pin, GPIO.OUT)
            # XOR with inverted
            GPIO.output(relay_pin, inverted != led_state)

            GPIO.setwarnings(True)
            if led_state:
                if cmd_on:
                    self._logger.info(
                        "Ocotrelay system command: {}".format(cmd_on))
                    os.system(cmd_on)
            else:
                if cmd_off:
                    self._logger.info(
                        "Ocotrelay system command: {}".format(cmd_off))
                    os.system(cmd_off)
            self.update_ui()
            return "ok"
        except Exception as e:
            self._logger.debug(e)
            return "error"

    def get_api_commands(self):
        return {
            "update": ["pin"],
            "getStatus": ["pin"],
            "listAllStatus": [],
        }

    def on_api_command(self, command, data):
        self._logger.debug("on_api_command {}, some_parameter is {}".format(command, data))

        # added api command to get led status
        if command == "listAllStatus":
            GPIO.setwarnings(False)
            active_relays = []
            for key in self.get_settings_defaults():
                settings = self._settings.get([key], merged=True)
                if settings["active"]:
                    relay_pin = int(settings["relay_pin"])
                    inverted = settings['inverted_output']
                    GPIO.setup(relay_pin, GPIO.OUT)
                    relay_data = dict(
                        id=key,
                        name=settings["labelText"],
                        active=inverted != GPIO.input(relay_pin),
                    )
                    active_relays.append(relay_data)
            return flask.jsonify(active_relays)

        # added api command to get led status
        if command == "getStatus":
            led_state = self.update_relay(data["pin"], get_status=True)
            return flask.jsonify(status=led_state)

        if command == "update":
            status = self.update_relay(data["pin"])
            return flask.jsonify(status=status)

    def on_event(self, event, payload):
        self._logger.debug("Got event: {}".format(event))
        if event == Events.CLIENT_OPENED:
            if hasattr(self, 'model'):
                self.update_ui()
        elif event == Events.PRINT_STARTED:
            self.print_started()
        elif event == Events.PRINT_DONE:
            self.print_stopped()
        elif event == Events.PRINT_FAILED:
            self.print_stopped()
        # elif event == Events.PRINT_CANCELLING:
        # self.print_stopped()
        # elif event == Events.PRINT_CANCELLED:
        # self.print_stopped()
        return

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.update_ui()

    def print_started(self):
        for off_timer in self.turn_off_timers:
            try:
                self.turn_off_timers[off_timer].cancel()
                self._logger.info("cancelled timer: {}".format(off_timer))
            except Exception:
                self._logger.warn("could not cancel timer: {}".format(off_timer))
        for index in self.model:
            settings = self._settings.get([index], merged=True)

            auto_on_for_print = settings['autoONforPrint']
            if auto_on_for_print:
                relay_pin = int(settings["relay_pin"])
                inverted = settings['inverted_output']

                GPIO.setup(relay_pin, GPIO.OUT)
                # XOR with inverted
                GPIO.output(relay_pin, inverted is not True)
        self.update_ui()

    def print_stopped(self):
        for index in self.model:
            settings = self._settings.get([index], merged=True)

            relay_pin = int(settings["relay_pin"])
            inverted = settings['inverted_output']
            auto_off_for_print = settings['autoOFFforPrint']
            auto_off_delay = int(settings['autoOffDelay'])
            cmd_off = settings['cmdOFF']
            active = settings["active"]
            if auto_off_for_print and active:
                self._logger.debug("turn off pin: {} in {} seconds. index: {}".format(
                    relay_pin, auto_off_delay, index))
                self.turn_off_timers[index] = ResettableTimer(
                    auto_off_delay, self.turn_off_pin, [relay_pin, inverted, cmd_off])
                self.turn_off_timers[index].start()
        self.update_ui()

    def turn_off_pin(self, relay_pin, inverted, cmd_off):
        GPIO.setup(relay_pin, GPIO.OUT)
        # XOR with inverted
        GPIO.output(relay_pin, inverted is not False)
        GPIO.setwarnings(True)
        if cmd_off:
            os.system(cmd_off)
        self._logger.info("pin: {} turned off".format(relay_pin))
        self.update_ui()

    def update_ui(self):
        settings = self.get_settings_defaults()
        for index in settings:
            settings[index].update(self._settings.get([index]))

            label_text = settings[index]["labelText"]
            active = int(settings[index]["active"])
            relay_pin = int(settings[index]["relay_pin"])
            inverted = settings[index]['inverted_output']
            icon_on = settings[index]['iconOn']
            icon_off = settings[index]['iconOff']
            confirm_off = settings[index]['confirmOff']

            # set the icon state
            GPIO.setup(relay_pin, GPIO.OUT)
            self.model[index]['relay_pin'] = relay_pin
            self.model[index]['state'] = GPIO.input(relay_pin)
            self.model[index]['labelText'] = label_text
            self.model[index]['active'] = active
            if inverted != self.model[index]['state']:
                self.model[index]['iconText'] = icon_on
                self.model[index]['confirmOff'] = confirm_off
            else:
                self.model[index]['iconText'] = icon_off
                self.model[index]['confirmOff'] = False

        # self._logger.info("update ui with model {}".format(self.model))
        self._plugin_manager.send_plugin_message(self._identifier, self.model)

    def process_at_command(self, comm_instance, phase, command, parameters, tags=None, *args, **kwargs):
        if command == "OCTORELAY":
            index = parameters
            self.update_relay(index)
            return None

    def get_update_information(self):
        return dict(
            octorelay=dict(
                displayName="OctoRelay",
                displayVersion=self._plugin_version,

                type="github_release",
                current=self._plugin_version,

                user="borisbu",
                repo="OctoRelay",
                pip="https://github.com/borisbu/OctoRelay/archive/{target}.zip",

                stable_branch=dict(
                    name="Stable",
                    branch="master",
                    commitish=["master"]
                ),

                prerelease_branches=[dict(
                    name="Prerelease",
                    branch="develop",
                    commitish=["develop", "master"]
                )]
            )
        )

    # GPIO Polling thread
    def input_polling(self):
        self._logger.debug("input_polling")
        for index in self.model:
            if self.model[index]['active'] and GPIO.input(self.model[index]['relay_pin']) != self.model[index]['state']:
                self.update_ui()
                break


__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = OctoRelayPlugin()

__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
    "octoprint.comm.protocol.atcommand.sending": __plugin_implementation__.process_at_command
}
