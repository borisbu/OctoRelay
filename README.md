# OctoRelay
A plugin that adds buttons to the navigation bar to toggle GPIO pins on the Raspberry Pi.

This Plugin is based on the Octolight Plugin by Žiga Kralj (https://github.com/gigibu5/OctoLight) thanks ;-)

![WebUI interface](img/screenshoot.png)

## Setup
Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

	https://github.com/borisbu/OctoRelay/archive/master.zip

## Configuration
![Settings panel](img/settings.png)

Curently, you can configure two settings:
- `Light PIN`: The pin on the Raspberry Pi that the button controls.
	- Default value: 13
	- The pin number is saved in the **board layout naming** scheme (gray labels on the pinout image below).
	- **!! IMPORTANT !!** The Raspberry Pi can only controll the **GPIO** pins (orange labels on the pinout image below)
	![Raspberry Pi GPIO](img/rpi_gpio.png)

- `Inverted output`: If true, the output will be inverted
	- Usage: if you have a light, that is turned off when voltage is applied to the pin (wired in negative logic), you should turn on this option, so the light isn't on when you reboot your Raspberry Pi.

## TO DO
- [ ] Update interface if Light is turned on or off

Maybe in the distant future:
- [ ] Turn off on finish print
