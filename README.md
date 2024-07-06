# OctoRelay

[![CI](https://github.com/borisbu/OctoRelay/actions/workflows/CI.yaml/badge.svg)](https://github.com/borisbu/OctoRelay/actions/workflows/CI.yaml)
[![CodeQL](https://github.com/borisbu/OctoRelay/actions/workflows/codeql.yml/badge.svg)](https://github.com/borisbu/OctoRelay/actions/workflows/codeql.yml)
[![Coverage Status](https://coveralls.io/repos/github/borisbu/OctoRelay/badge.svg?branch=master)](https://coveralls.io/github/borisbu/OctoRelay?branch=master)
[![Downloads of latest release](https://img.shields.io/github/downloads/borisbu/octorelay/latest/release.zip?color=blue)](https://github.com/borisbu/OctoRelay/releases/latest)

The plugin adds buttons to control GPIO pins of Raspberry Pi for switching relays and indicating their states.

![WebUI interface](img/controls.png)

In this screenshot, the black printer icon shows the `ON` state of its relay, and the gray ones indicate `OFF`.
The plugin allows you to set your own icons and flexibly customize the way the relay states are displayed.

> _I use it with a 4 relay board, and printed this
> [case for it](https://www.thingiverse.com/thing:2975944)._
> _Just hooked up the GPIO pins with the relay board, and now I can turn the
> power of the printer, the fan and the light on and off with OctoPrint._
>
> _This plugin was based on the [OctoLight Plugin](https://github.com/gigibu5/OctoLight) by Žiga Kralj, thanks ;-)_
>
> — _Boris Burgstaller_

| ![Relay Board](img/relay.jpg) | ![Raspberry Pi GPIO](img/gpio.png) |
|-------------------------------|------------------------------------|

## Requirements

- Python: at least `3.8`,
- OctoPrint: at least `1.5.3`.
  - For [AutoConnect feature](https://github.com/borisbu/OctoRelay/blob/master/CHANGELOG.md#330): at least `1.9.0`.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

```
https://github.com/borisbu/OctoRelay/releases/latest/download/release.zip
```

In case you want to enable the plugin for user groups other than admins and users (operators), you need to
grant them the permission "Relay switching" in the "Access control" section of OctoPrint settings.

After installing the plugin you need to configure it in order to see the control buttons in the navigation bar.

## Configuration

![Settings panel](img/settings.png)

Currently, OctoRelay supports up to 8 relays represented by the tabs on the top of the settings screen.
Each relay has the following settings *(in order of appearance)*:

| Setting                 | Description                                                      |
|-------------------------|------------------------------------------------------------------|
| Active                  | Activates the relay control and indication on the navigation bar |
| Label                   | The relay description to show on tooltip and in dialogs          |
| Icon `ON` / `OFF`       | An image or emoji to indicate the relay state (supports HTML)    |
| This is printer relay   | Closes the printer connection when turning this relay `OFF`      |
| AutoConnect delay       | Printer relay feature adjustment when turning it `ON`            |
| GPIO Number             | The [GPIO pin on the Raspberry Pi](https://pinout.xyz/)          |
| Inverted output         | For normally closed relay: the relay is `ON` without power       |
| Confirm turning `OFF`   | Enables a confirmation dialog when turning the relay `OFF`       |
| Alert on switches ahead | Notifies on upcoming switch with an ability to cancel it         |
| **Events:**             | Behavior customization (automation)                              |
| on Startup              | The state to switch the relay to when OctoPrint started          |
| on Printing Started     | The state to switch the relay to when started printing           |
| on Printing Stopped     | The state to switch the relay to when stopped printing           |
| after Turned `ON`       | The state to switch the relay to after it has been turned `ON`   |
| skip *(option)*         | No action should be taken                                        |
| delay                   | Postpones the action for the time specified in seconds           |
| **Side effects:**       | Additional actions in certain cases                              |
| Command `ON` / `OFF`    | An optional OS command to run when toggling the relay            |

## Operation

You can toggle the relays ON and OFF the following ways:

- By clicking the control buttons on the navigation bar.
  - The icon you choose for the button will display the current state.
- By sending GCODE command `@OCTORELAY r# [ON|OFF]`.
  - Where `#` is relay index from `1` to `8`;
  - While `[ON|OFF]` is an optional target.
- Or by querying the API (see below).

## OctoRelay API

Relays can be queried and updated through the [OctoPrint API](https://docs.octoprint.org/en/master/api/). Read that documentation on how to get an API Key.

### Change the relay state

This query turns the relay `r1` OFF:

```bash
curl 'http://octopi.local/api/plugin/octorelay' \
  -H 'X-Api-Key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{ "command": "update", "subject": "r1", "target": false }'

# Sample response:
# {
#   "status": false
# }
```

The `target` entry in request payload is an optional boolean parameter. When it's `null` or omitted the relay will toggle. The `status` entry in the response payload reflects the relay state as the outcome of the request.

### Request the relay state

This query provides the status or the relay `r1`:

```bash
curl 'http://octopi.local/api/plugin/octorelay' \
  -H 'X-Api-Key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{ "command": "getStatus", "subject": "r1" }'

# Sample response:
# {
#   "status": true
# }
```

### List all the relay states

This query provides the statuses of all the relays:

```bash
curl 'http://octopi.local/api/plugin/octorelay' \
  -H 'X-Api-Key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{ "command": "listAllStatus" }'

# Sample response:
# [
#   {
#     "status": true,
#     "id": "r1",
#     "name": "Light"
#   },
#   {
#     "status": false,
#     "id": "r2",
#     "name": "Printer"
#   }
# ]
```

The `status` entry reflects the actual state of the relay.

## Updates

Check out the versions, their features and bug fixes in the [Changelog](CHANGELOG.md).
