# OctoRelay
A plugin that adds buttons to the navigation bar to toggle GPIO pins on the Raspberry Pi.

This Plugin was based on the Octolight Plugin by Žiga Kralj (https://github.com/gigibu5/OctoLight) thanks ;-)

![WebUI interface](img/screenshot.png)

I use it with a 4 relay board, and printed this case for it:
https://www.thingiverse.com/thing:2975944

![Relay Board](img/relay-raspberry.jpg)



just hooked up the GPIO pins with the relay board, and now I can turn the power of the printer, the fan and the light on and foo with OctoPrint.

![Raspberry Pi GPIO](img/rpi_gpio.png)

## Setup
Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

	pip install https://github.com/borisbu/OctoRelay/archive/master.zip

## Configuration
![Settings panel](img/settings.png)

Curently, OctoRelay supports up to 8 relays:


| key | value |
|--|--|
| Relay X active | if true, this relay is active. If false, it will disappear in the settings and the navigation bar |
| Relay PIN | the GPIO pin on the Raspberry pi (see the picture above) |
| On on boot | if ticked this pin will be set to ON on start |
| Inverted output | if ticked the output on the pin is inverted (ex. relays is ON if GPIO pi is GND and OFF if GPIO pin is 3.3V) |
| Icon On | piece of html output if the relay is ON (can be text, img...)|
| Icon Off | piece of html output if the relay is OFF |
| Label | the html title of the icon in the navbar (text if you hover the icon) |

