# Changelog

## Version 3

### 3.2.1

- A minor technical refactoring.
  - Using relative imports in the plugin class file.

### 3.2.0

- This release fixes a UX bug for new installations found and reported by [@kds69](https://github.com/kds69).
  - When installing the plugin first time first 4 relays used to be activated by default having sample configuration.
  - From now on all relays are deactivated by default to prevent unexpected side effects.
- For existing installations this release introduces a new feature — the plugin settings migration.
  - This update will migrate the existing plugin settings and preserve the activity state of the fist 4 relays.

### 3.1.1

- Changed the payload produced by `update_ui()` method:
  - `active` — type ~~`(int)`~~ changed to `(bool)`.

### 3.1.0

- Operating GPIO and obtaining relay state was extracted into the Relay driver.
- Executing OS commands was extracted into a dedicated method.
- Moved tests out of the distribution.
- Changed the payload produced by `update_ui()`:
  - ~~`state (int)`~~ — the pin state, removed
  - `inverted_output (bool)` — added
  - `relay_state (bool)` — added.

### 3.0.1

- Fixed issue on partial saving of the plugin settings.
- Refactoring: enforcing code style for Python using `pylint`.
- Testing and clarifying the actual plugin compatibility with OctoPrint.
  - Minimum supported version of OctoPrint is 1.5.3.

### 3.0.0

- **Breaking changes**
  - Changing the release type to a distributable package.
  - Plugin version is now set automatically from a GitHub release using `miniver`.
  - A workflow creates a package and then attaches it to the release assets.
  - Thus, redundant files are removed from the distribution.
  - The latest release distribution URL has changed to
    `https://github.com/borisbu/OctoRelay/releases/latest/download/release.zip`
  - Once you upgrade the plugin from v2 or v1 you will see that the control buttons are gone.
  - Instead, there will be a warning button ⚠️ having instructions on further steps:
    1. Don't panic.
    2. Please proceed to "Software update" section of the OctoPrint settings.
    3. Find the OctoRelay plugin showing `Installed: unknown` — this is expected.
    4. There also should be a button to UPDATE the plugin one more time.
    5. After that the plugin will be updated from the new distribution URL and the control buttons appear again.
  - Sorry for the inconvenience.
    - In case there is no button to update, use the "Force check for updates" function on the top.
    - As a last resort you can always use the URL mentioned above to reinstall the plugin manually.

![Update button](https://user-images.githubusercontent.com/13189514/257075791-460da3a9-c814-4d5e-b577-31c739bd3e67.png)

## Version 2

### 2.2.5

- Hotfix: partial revert of changes from version 2.2.2.
  - On some OctoPrint installations the values of plugin settings did not appear.
  - It has been experimentally established that restoring the templates array as an inline return might fix this issue.

### 2.2.4

- Fixed UI/UX bug.
  - Hover state made responsive, similar to native OctoPrint buttons.
  - Emoji-based buttons are enlarged slightly in order to align with image-based ones.
  - Buttons alignment and consistency improved:
    - Each button is now `40x40px`,
    - Each emoji on the button is now `1.25rem` which is `20px`,
    - Each image on the button is expected to be `24x24px`.

![UI Controls](https://github.com/borisbu/OctoRelay/assets/13189514/4e594ef9-0547-4a2b-95b3-5050971bc973)

### 2.2.3

- Refactoring.
  - Using `f"string"` syntax instead of `"".format()`.
  - Strict handling of booleans.

### 2.2.2

- Another technical update.
  - Simplified iteration through relay settings and eliminated some redundant method calls.

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
