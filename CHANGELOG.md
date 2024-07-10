# Changelog

## Version 5

### 5.0.0

- **Breaking changes**:
  - Minimum version of Python supported: 3.9;
- Feature: Supporting Raspberry Pi 5:
  - Using `gpiozero` with two `lgpio` and `RPi.GPIO` factories depending on your hardware;
  - The feature implemented by [Mattia Vidoni](https://github.com/ch3p4ll3)

## Version 4

### 4.2.1

- Technical update: 
  - Reduced number of dependencies;
  - Upgraded testing framework;
  - Removed a redundant statement. 

### 4.2.0

- Supporting OctoPrint 1.10 and Python 3.12.

### 4.1.0

- New feature: target for GCODE command (at-command):
  - You can now switch the relay to the desired state;
  - `@OCTORELAY r1 ON` — to switch the first relay on;
  - `@OCTORELAY r1 OFF` — to switch the first relay off;
  - `@OCTORELAY r1` — to toggle the first relay.

### 4.0.1

- Technical update: no new features, no fixes.

### 4.0.0

- **Breaking changes**:
  - Plugin API v1 removed.
- How to migrate confidently:
  - If you're not using the plugin API or mobile applications that use the plugin API:
    - No action required.
  - Read the release notes for version 3.14.0 (below) to inform yourself on differences between API v1 and v2.
  - If you're using API v1:
    - Make sure you're using OctoRelay version 3.14.0 or upgrade to that version first,
    - Rename `pin` parameter in your request payload to `subject`,
    - Add `version: 2` or `v: 2` parameter to all your API requests,
    - Expect to receive a response having HTTP status code `200` and handle others as failures,
    - In response to `listAllStatus` command expect to receive `status` (boolean) instead of `active`,
    - In response to `update` command expect to receive boolean `status` instead of "ok" string,
    - In response to `cancelTask` command expect to receive `cancelled` (boolean) instead of `status`,
    - Test all your API requests before upgrading.
  - If you're using [OctoPod, iOS/tvOS/watchOS App](https://apps.apple.com/us/app/octopod-for-octoprint/id1412557625):
    - Upgrade it to at least 3.27 — this version supports the plugin API v2 (and v1 too).
  - After upgrading to this version:
    - You can remove `version` or `v` argument from the request payload (no longer needed).
- Other improvements:
  - UI: Upgraded all dependencies.

## Version 3

### 3.14.0

- UI: Generating CSS from SCSS.
- Using `mypy` for type constraints.
- Introducing the plugin API v2.
  - This feature aims to establish consistency and improve clarity across inputs and responses of the plugin API.
  - This feature is opt-in until the next major release of the plugin.
  - Developers and other API users are advised to migrate to the new API.
  - Introducing the `version` and its shorthand `v` parameter of each API request payload (integer).
    - When the parameter is ommitted, the API falls back to v1 (previous behaviour and responses).
    - When the parameter is set to `2`, the new request payload is expected and the API responds differently.
  - Main differences of v2:
    - For `update` and `getStatus` commands `pin` parameter is renamed to `subject`.
    - For `listAllStatus` command `active` property renamed to `status`.
    - For `getStatus` command on disabled relay the API responds with an HTTP code `400` instead of `status: false`.
    - For `update` and `cancelTask` commands there is no more `status: "ok" | "error"`:
      - The `status` now always means the relay state (boolean), while errors are reported via HTTP codes.
  - Check out the updated Readme for new examples.

| Command       | v1 request parameters    | v2 request parameter     |
|---------------|--------------------------|--------------------------|
| update        | `pin, target`            | `subject, target`        |
| getStatus     | `pin`                    | `subject`                |
| listAllStatus | None                     | None                     |
| cancelTask    | `subject, target, owner` | `subject, target, owner` |

| Command       | v1 response                | v2 response          |
|---------------|----------------------------|----------------------|
| update        | `result: bool, status: ok` | `status: bool`       |
| getStatus     | `status`                   | `status`             |
| listAllStatus | `[active, id, name]`       | `[status, id, name]` |
| cancelTask    | `status: ok`               | `cancelled: bool`    |

### 3.12.0

- Feature: the API command `update` now accepts the optional `target` parameter.
  - Check out the updated documentation in Readme for the request samples and more details.
  - Thanks to [@patrickcollins12](https://github.com/patrickcollins12) for that contribution.

### 3.11.2

- UI source code splitting.
  - Making the code easier to test and to maintain.

### 3.11.1

- Removing the stub `js` file from the sources.
  - The plugin should only be installed from the distributed release file (not from the sources).
- Changing the UI compiler from `tsc` to `tsup` (based on `esbuild` and `rollup`).
- Extracting the types into the dedicated files.

### 3.11.0

- UI improvement: better handling of multiple upcoming switches.
  - No overlapping popovers: single popover for all upcoming events instead.
  - Sorted by the time left.
  - Assigned to the relay having the closest switching.

![UI](https://user-images.githubusercontent.com/13189514/270194227-b763214f-d237-4d0e-aab8-78de3215fb45.png)

### 3.10.0

- New feature: AutoConnect delay setting.
  - Only visible for a Printer Relay (another setting).
  - Only functional for OctoPrint 1.9.0+.

### 3.9.1

- Renamed setting: "Confirm turning OFF".
- Fixed issue found and reported by [@CrNMGuy](https://github.com/CrNMGuy).
  - When printing started should cancel a postponed switch caused by Printing
    Stopped event.

### 3.9.0

- A small performance improvement.
  - When handling the events causing the relay switches, now triggering the UI
    update only once for them all after processing their new state.
- New setting: "This is printer relay".
  - Ability to specify the relay that controls your printer.
  - Thus, the plugin can distinguish the printer relay among other ones.
  - The migration script will set this setting to `r2` if you didn't change the
    second relay label `Printer` (default).
  - You may quite reasonably wonder why this is needed:
- New feature: AutoDisconnect.
  - Disconnects from the printer before turning its relay off
    (according to the new setting).
  - This helps to shut down the printer a bit more gracefully.
  - It prevents an error state like `SerialException` when turning printer off.
- A small improvement to the AutoConnect feature in this regard.
  - Now connects automatically only when there are some ports available.
  - This also prevents the failures to AutoConnect and attempts to reconnect
    after turning the printer relay off.

![UI](https://user-images.githubusercontent.com/13189514/268201477-01688f8d-08ed-4d1f-8c71-8f278b8f7f04.png)

### 3.8.2

- Fixed a bug: the popover on upcoming relay switch could not appear in some cases.
  - In case a postponed switch is configured for PRINTING_STARTED or PRINTING_STOPPED event, but no switch is
    configured to happen immediately, the UI did not have an update.
  - Thanks to [@backupartist](https://github.com/backupartist) for reporting and elaborating to fix this issue.

### 3.8.1

- A couple fixes for the upcoming switch popover:
  - The outside clicks handler is removed, so dismissing the popover is now only possible by clicking the Close button.
  - Restoring the regular tooltip after dismissing the popover.

### 3.8.0

- Improved logging:
  - fewer messages on `info` level,
  - more messages on `debug` level.
- Introducing the new event: After Turned ON.
  - By setting the option to `OFF` with a certain delay, now it has become
    possible to turn on something for a limited time, not related to printing.

### 3.7.2

- This update prohibits switching of disabled relays.

### 3.7.1

- Fixed a bug: the disabled relays were still requested on their pin states.

### 3.7.0

- Introducing the ability to cancel the upcoming automated switch.
  - In case of a configured relay switching delay, the corresponding
    control button will notify about this in a popover.
  - The popover shows the upcoming state and the countdown.
  - The popover offers a Cancel button to dismiss the pending task.
  - This feature is opt-out and can be disabled in the plugin settings.
- New relay setting: "Alert on switches ahead".

![UI](https://user-images.githubusercontent.com/13189514/260525275-dae7b391-71a1-4624-a235-27aa825996a7.png)

### 3.6.0

- Tooltips for control buttons.

![Controls](https://user-images.githubusercontent.com/13189514/260209663-73146715-5f42-471b-a6cb-a0d82f894b3c.png)

### 3.5.0

- A couple more improvements for the UI/UX.
  - This version introduces a new asset — CSS file.

![UI](https://user-images.githubusercontent.com/13189514/260043096-38e10e10-1285-401f-bf1f-18aa9e397c25.png)

### 3.4.0

- New feature: event-based automation.
  - In the new UI you can now specify the desired relay state for three events:
    - on Startup,
    - on Printing Started
    - on Printing Stopped.
  - Relay switching actions can also be skipped or postponed.
  - In particular, it enables you to turn something ON after printing, which
    was not possible before.
- This update will migrate the relay settings in existing configuration.
- New UI offers radio buttons instead of checkboxes and distributes the relay
  settings across tabs.

![UI](https://user-images.githubusercontent.com/13189514/259849257-9199e3f1-50f3-4ef9-9245-6c04e544db7d.png)

| Before                 | After                          | Type           |
|------------------------|--------------------------------|----------------|
| `initial_value`        | `rules.STARTUP.state`          | `bool or None` |
| `auto_on_before_print` | `rules.PRINTING_STARTED.state` | `bool or None` |
| `auto_off_after_print` | `rules.PRINTING_STOPPED.state` | `bool or None` |
| `auto_off_delay`       | `rules.PRINTING_STOPPED.delay` | `int`          |

### 3.3.2

- Refactoring: using `merged=True` option for consistent retrieval of the relay settings.

### 3.3.1

- Refactoring: consistent naming for the plugin settings.
  - This update will migrate the relay settings in existing configuration.

| Before            | After                  |
|-------------------|------------------------|
| `labelText`       | `label_text`           |
| `cmdON`           | `cmd_on`               |
| `cmdOFF`          | `cmd_off`              |
| `autoONforPrint`  | `auto_on_before_print` |
| `autoOFFforPrint` | `auto_off_after_print` |
| `autoOffDelay`    | `auto_off_delay`       |
| `iconOn`          | `icon_on`              |
| `iconOff`         | `icon_off`             |
| `confirmOff`      | `confirm_off`          |

### 3.3.0

- New feature: AutoConnect.
  - After turning the printer relay ON the plugin will initiate the connection to printer automatically.
  - The feature is only available to users of OctoPrint starting version 1.9.0.

### 3.2.1

- A minor technical refactoring.
  - Using relative imports in the plugin class file.

### 3.2.0

- This release fixes a UX bug for new installations found and reported by [@kds69](https://github.com/kds69).
  - When installing the plugin first time, first 4 relays used to be activated by default having sample configuration.
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
