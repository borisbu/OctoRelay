# Changelog

## Version 2

### 2.2.1

- Technical update: no fixes or new features.
  - Adaptation of a method for possible future changes.
  - Minor refactoring.

### 2.2.0

- Thanks to [@jneilliii](https://github.com/jneilliii)'s contribution, the plugin supports GCODE command `@OCTORELAY`.
  - The command toggles the relay by its index specified in parameters.
  - Currently supported indexes are from `r1` to `r8`.
  - Example: `@OCTORELAY r4`.
  - Documentation on `@` commands: https://docs.octoprint.org/en/master/features/atcommands.html

### 2.1.0

- This version contains an important security fix:
  - Read only users are prohibited from switching the relays.
  - Thanks to [@plazarch](https://github.com/plazarch) for reporting the important security flaw.
- This version introduces a custom permission: "Relay switching".
  - The following groups are granted that permission by default: admins and users (operators).
  - You can allow relay switching to other ones in "Access control" section of OctoPrint settings.

### 2.0.2

- Fixed missing requirement on the `pin` parameter for API commands `update` and `getStatus`.
  - Thanks to [@jneilliii](https://github.com/jneilliii) for the contribution.

### 2.0.1

- Fixed turning non-inverted relays ON and executing the corresponding optional OS Command when start printing.
  - Thanks to [@NDR008](https://github.com/NDR008) contribution, the issue
    [#46](https://github.com/borisbu/OctoRelay/issues/46) most is likely resolved.
- Fixed incorrect description of OS Command setting in the documentation.
- Plugin executable code now has `99%` test coverage.
  - All following contributions, features and fixes should take this into account.
  

### 2.0.0

- **Breaking changes**
  - Minimal Python version required: `3.7`.
  - Minimal JavaScript version support required: `ES6` (aka ES2015).
    - Minimal browser versions supporting ES6 are listed [here](https://caniuse.com/?search=es6).
  - The distributed PNG icons are replaced with SVG ones.
    - In case you've been using them in your configuration (`Icon ON/OFF`), you need to change their filenames:
      - `3d-printer.png` –> `3d-printer.svg`,
      - `fan-24.png` –> `fan.svg`,
      - `webcam.png` –> `webcam.svg`.
    - `refresh.png` icon is removed from the distribution.

## Version 1

### 1.4.2

- Fixed `height` property of the icons in the initial config.

### 1.4.1

- Fixed issue with turning relays ON when start printing.
  - Thanks to [@hcooper](https://github.com/hcooper)'s contribution issues
    [#39](https://github.com/borisbu/OctoRelay/issues/39) and
    [#52](https://github.com/borisbu/OctoRelay/issues/52) are most likely resolved.

### 1.4.0

- JS: Types constraints and tests.
- Moving JS from template.
- Plugin description update.

### 1.3.0

- Making a pre-release channel.
- Updating the documentation.

### 1.2.0

- Add API command to get all the states at once.

### 1.1.1

- Add API command to get pin status `{'pin': 'r1', 'command': 'getStatus'}`.
- Poll GPIO to update the UI if the state changes in the background.

### 1.1.0

- Optional confirmation dialog when turning OFF.
- Auto ON/OFF on start and finish of the print job.
- Auto OFF delay for a fan, that should run longer after the print finished.

### 1.0.0

- Turn relays on and off.
- Changing icon.
- Power ON on boot.
