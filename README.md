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

	https://github.com/borisbu/OctoRelay/archive/master.zip

## Configuration
![Settings panel](img/settings.png)

Curently, OctoRelay supports up to 8 relays:


| key | value |
|--|--|
| Relay X active | if true, this relay is active. If false, it will disappear in the settings and the navigation bar |
| GPIO Number | the GPIO pin on the Raspberry pi (see the picture above) |
| On on boot | if ticked this pin will be set to ON on start |
| Inverted output | if ticked the output on the pin is inverted (ex. relays is ON if GPIO pi is GND and OFF if GPIO pin is 3.3V) |
| Icon On | piece of html output if the relay is ON (can be text, img...)|
| Icon Off | piece of html output if the relay is OFF |
| Label | the html title of the icon in the navbar (text if you hover the icon) |
| Confirm | if ticked, a confirmation dialog shows before turning the relay off |
| Auto ON/OFF |  |
| Auto ON before printing | Turn the relay automatically ON if a print starts |
| Auto OFF after print finishes | Turn the relay OFF after a print finishes |
| Auto OFF delay | Wait for X seconds before turning OFF the relay automatically. For exampe for a fan that should run a bit longer |

## Versions/Features/Bugfixes

1.0.0

- turn relays on and off
- change icon
- power on on boot

1.1.0

- optional confirm dialog on turning OFF
- Auto ON/OFF on start and finish of the print job
- Auto OFF delay for a fan, that should run longer after the print finished

1.1.1

- Add api command to get pin status {'pin': 'r1', 'command': 'getStatus'}
- Poll GPIO to update the UI if the state changes in the backround

1.2.0

- Add api command to get all the states at once

1.3.0 ? 2.0 ?

- Extended GPIO/Relay Support using a Relay Plugins Module
- Additional config options to select plugin.
- Currently supports:
 - "<default>" (no attributes) - same as "GPIO".
 - "GPIO"      (no attributes) - use the default Raspberry Pi's onboard GPIOs.
 - "ProXr"     (<serial device>) - use a Relay board that supports the ProXr command protocol.
- Easy extension of GPIO/Relay Modules by adding new plugins (see mRBase.py example)
- Plugins registered using relay_register.json

Additional Info on "ProXr" module:
- Relay board sometimes un-responsive, see logging info below for a fix.
- Logging may show errors such as: device reports readiness to read but returned no data
  If so then use the following to turn off getty on the underlying port:
  user:~ $ sudo systemctl stop serial-getty@tty<USBn>.service
  user:~ $ sudo systemctl mask serial-getty@tty<USBn>.service
    where USBn is the ttyUSB device number connected to the relay board.
  eg. (for /dev/ttyUSB0) :
    'sudo systemctl stop serial-getty@ttyUSB0.service'
    'sudo systemctl mask serial-getty@ttyUSB0.service'
  This creates a null symlink at /etc/systemd/system/<device> that can be deleted
  at a later date if the user wants to return the mounting of a TTY to this
  serial device (needed by login consoles but not by simple serial interfaces)
- Module Attributes (Full control). The atributes are a comma-separated string but
  all parameters beyond the device name are optional:
  <dev[,baud[,bits,par,stops]]>
  Defaults are: baud=115200, bits=8, par=N, stops=1
  Response timeout: this is hardcoded to 1 second.
  
