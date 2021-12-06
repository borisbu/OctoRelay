# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
from octoprint.events import Events
from octoprint.util import ResettableTimer
from octoprint.util import RepeatedTimer

# *NEW* Relay Driver Plugin module - supports multiple relay types
import relay_loader

import flask
import os

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

    ## OK
    def get_settings_defaults(self):
        return dict(
            driver=dict(
                # Note: Global driver plugin settings. Affects all relays.
                driver_id="<default>", # default is the RaspberryPi GPIO pins. To-Do : change to pulldown in GUI and read .json config?
                driver_attr=""
            ),
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
                active = True,
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

    ## OK - noactionneeded
    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

    ## OK - noactionneeded
    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/octorelay.js"],
        )

    ## OK
    def on_after_startup(self):
        self._logger.info("--------------------------------------------")
        self._logger.info("start OctoRelay")

        self.model = dict()
        self.turn_off_timers = dict()
        self.driver = None # loaded plugin driver

        settings = self.get_settings_defaults()

        # find and update the global section first. includes loading the 
        # requested relay driver plugin, needed by all enabled relays.
        settings['driver'].update(self._settings.get(['driver']))
        if 'driver' in settings:
            self._logger.debug("settings for global relay driver: {}".format(settings['driver']))
            d_id = settings['driver']['driver_id']
            d_attr = settings['driver']['driver_attr']
            self.driver = relay_loader.instantiate_relay_object(d_id)
            if self.driver == None:
                self._logger.error("Invalid Relay driver plugin ID : {}".format(d_id))
            else:
                self._logger.debug("Using relay driver plugin: {}".format(d_id))
                self.driver.open(d_attr) # open plugin, with configured attributes (if needed)
                
        else:
            self._logger.error("Missing global relay configuration settings! (driver)")

        for index in settings:
            if index != 'driver':
                settings[index].update(self._settings.get([index]))
                self._logger.debug("settings for {}: {}".format(index, settings[index]))
                self.model[index] = dict()
                if settings[index]['active']:
                    relay_pin = int(settings[index]['relay_pin'])
                    initial_value = settings[index]['initial_value']
                    inverted_output = settings[index]['inverted_output']
                    if self.driver != None:
                        # Setting the default state of pin
                        # XOR with inverted
                        self.driver.relaySet(relay_pin, initial_value != inverted_output)
                        # Note: For plugin methods, first time a gpio is 
                        #       used, the pin is setup. Eg. RPi GPIO is
                        #       set to OUTPUT (setup is unique to each plugin)

        self.update_ui()
        self.polling_timer = RepeatedTimer(POLLING_INTERVAL, self.input_polling, daemon=True)
        self.polling_timer.start()

        self._logger.info("OctoRelay plugin started")
        self._logger.info("--------------------------------------------")

    ## OK
    def on_shutdown(self):
        self.polling_timer.cancel()
        if self.driver != None:
            self.driver.close()
            self.driver = None
        self._logger.info("OctoRelay plugin stopped")
        self._logger.info("--------------------------------------------")

    ## OK - noactionneeded
    def get_api_commands(self):
        return {
            "update": [],
            "getStatus": [],
            "listAllStatus":[],
        }

    ## OK
    def on_api_command(self, command, data):
        self._logger.debug("on_api_command {}, some_parameter is {}".format(command,data))

        # added api command to get led status
        if command == "listAllStatus":
            GPIO.setwarnings(False)
            activeRelays = []
            for key in self.get_settings_defaults():
                if key != 'driver':
                    settings = self.get_settings_defaults()[key]
                    settings.update(self._settings.get([key]))
                    if settings["active"]:
                        relay_pin = int(settings["relay_pin"])   
                        inverted = settings['inverted_output']
                        gpio_state = False # if something wrong in driver setup then raw input will read False
                        if self.driver:
                            ## GPIO.setup(relay_pin, GPIO.OUT)
                            gpio_state = self.driver.relayGet(relay_pin)
                        relaydata = dict(
                            id=key,
                            name=settings["labelText"],
                            active=inverted != gpio_state
                        )
                        activeRelays.append(relaydata)
            return flask.jsonify(activeRelays)

        index = data['pin']

        settings = self.get_settings_defaults()[index]
        settings.update(self._settings.get([index]))

        relay_pin = int(settings["relay_pin"])
        inverted = settings['inverted_output']
        cmdON = settings['cmdON']
        cmdOFF = settings['cmdOFF']

        ## GPIO.setwarnings(False)
        ## GPIO.setup(relay_pin, GPIO.OUT)
        ## # XOR with inverted
        ## ledState = inverted != GPIO.input(relay_pin)
        gpio_state = False # if something wrong in driver setup then raw input will read False
        if self.driver:
            gpio_state = self.driver.relayGet(relay_pin)
        ledState = inverted != gpio_state
            
        # added api command to get led status
        if command == "getStatus":
            return flask.jsonify(status=ledState)
            
        else:
            self._logger.debug("Ocotrelay before pin: {}, inverted: {}, currentState: {}".format(
                relay_pin,
                inverted,
                ledState
            ))

            # toggle state
            ledState = not ledState

            ## GPIO.setup(relay_pin, GPIO.OUT)
            ## # XOR with inverted
            ## GPIO.output(relay_pin, inverted != ledState)
            if self.driver:
                self.driver.relaySet(relay_pin, inverted != ledState)

            ## GPIO.setwarnings(True)
            
            if ledState:
                if cmdON:
                    self._logger.info(
                        "Ocotrelay system command: {}".format(cmdON))
                    os.system(cmdON)
            else:
                if cmdOFF:
                    self._logger.info(
                        "Ocotrelay system command: {}".format(cmdOFF))
                    os.system(cmdOFF)
            
            self.update_ui()
            return flask.jsonify(status="ok")

    ## OK - noactionneeded
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
        #elif event == Events.PRINT_CANCELLING:
            # self.print_stopped()
        #elif event == Events.PRINT_CANCELLED:
            # self.print_stopped()
        return

    ## OK - noactionneeded
    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.update_ui()

    ## OK
    def print_started(self):
        for off_timer in self.turn_off_timers:
            try:
                self.turn_off_timers[off_timer].cancel()
                self._logger.info("cancelled timer: {}".format(off_timer))
            except:
                self._logger.warn("could not cancel timer: {}".format(off_timer))
        for index in self.model:
            settings = self.get_settings_defaults()[index]
            settings.update(self._settings.get([index]))

            autoONforPrint = settings['autoONforPrint']
            if autoONforPrint:
                relay_pin = int(settings["relay_pin"])
                inverted = settings['inverted_output']

                ## GPIO.setup(relay_pin, GPIO.OUT)
                ## # XOR with inverted
                ## GPIO.output(relay_pin, inverted != True)
                if self.driver:
                    self.driver.relaySet(relay_pin, inverted != True)
                
        self.update_ui()

    ## OK
    def print_stopped(self):
        for index in self.model:
            settings = self.get_settings_defaults()[index]
            settings.update(self._settings.get([index]))

            relay_pin = int(settings["relay_pin"])
            inverted = settings['inverted_output']
            autoOFFforPrint = settings['autoOFFforPrint']
            autoOffDelay = int(settings['autoOffDelay'])
            cmdOFF = settings['cmdOFF']
            active = settings["active"]
            if autoOFFforPrint and active:
                self._logger.debug("turn off pin: {} in {} seconds. index: {}".format(
                    relay_pin, autoOffDelay, index))
                self.turn_off_timers[index] = ResettableTimer(
                    autoOffDelay, self.turn_off_pin, [relay_pin, inverted, cmdOFF])
                self.turn_off_timers[index].start()
        self.update_ui()

    ## OK
    def turn_off_pin(self, relay_pin, inverted, cmdOFF):
        ## GPIO.setup(relay_pin, GPIO.OUT)
        ## # XOR with inverted
        ## GPIO.output(relay_pin, inverted != False)
        ## GPIO.setwarnings(True)
        if self.driver != None:
            self.driver.relaySet(relay_pin, inverted != False)
        if cmdOFF:
            os.system(cmdOFF)
        self._logger.info("pin: {} turned off".format(relay_pin))
        self.update_ui()

    ## OK
    def update_ui(self):
        settings = self.get_settings_defaults()
        for index in settings:
            if index != 'driver':
                settings[index].update(self._settings.get([index]))

                labelText = settings[index]["labelText"]
                active = int(settings[index]["active"])
                relay_pin = int(settings[index]["relay_pin"])
                inverted = settings[index]['inverted_output']
                iconOn = settings[index]['iconOn']
                iconOff = settings[index]['iconOff']
                confirmOff = settings[index]['confirmOff']

                # set the icon state
                #GPIO.setup(relay_pin, GPIO.OUT)
                r_state = False
                if self.driver != None:
                    r_state = self.driver.relayGet(relay_pin)
                
                self.model[index]['relay_pin'] = relay_pin
                self.model[index]['state'] = r_state ## GPIO.input(relay_pin)
                self.model[index]['labelText'] = labelText
                self.model[index]['active'] = active
                if inverted != self.model[index]['state']:
                    self.model[index]['iconText'] = iconOn
                    self.model[index]['confirmOff'] = confirmOff
                else:
                    self.model[index]['iconText'] = iconOff
                    self.model[index]['confirmOff'] = False

        #self._logger.info("update ui with model {}".format(self.model))
        self._plugin_manager.send_plugin_message(self._identifier, self.model)

    ## OK - noactionneeded
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

    # OK
    # GPIO Polling thread
    def input_polling(self):
        self._logger.debug("input_polling")
        for index in self.model:
            r_state = False
            relay_pin = self.model[index]['relay_pin']
            if self.driver != None:
                r_state = self.driver.relayGet(relay_pin)
            ## if self.model[index]['active'] and GPIO.input(self.model[index]['relay_pin']) != self.model[index]['state']:
            if self.model[index]['active'] and r_state != self.model[index]['state']:
                self.update_ui()
                break

__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = OctoRelayPlugin()

__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config":
        __plugin_implementation__.get_update_information
}
