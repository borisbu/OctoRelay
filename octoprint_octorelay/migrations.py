# -*- coding: utf-8 -*-
def v0(settings, logger):
    """Migration from v0 to v1"""
    # First 4 relays used to have active=True
    for index in ["r1", "r2", "r3", "r4"]: # no references to constants
        before = settings.get([index]) # without defaults
        logger.debug(f"relay {index} stored settings: {before}")
        if "active" not in before:
            logger.debug("inserting active=True into it")
            after = { **before, "active": True }
            settings.set([index], after)

def v1(settings, logger):
    """Migration from v1 to v2"""
    # Some settings were named in camelCase
    replacements = {
        "labelText": "label_text",
        "cmdON": "cmd_on",
        "cmdOFF": "cmd_off",
        "autoONforPrint": "auto_on_before_print",
        "autoOFFforPrint": "auto_off_after_print",
        "autoOffDelay": "auto_off_delay",
        "iconOn": "icon_on",
        "iconOff": "icon_off",
        "confirmOff": "confirm_off"
    }
    for index in ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]: # no references to constants
        before = settings.get([index]) # without defaults
        after = {}
        logger.debug(f"relay {index} stored settings: {before}")
        for key, value in before.items():
            if key in replacements:
                after[replacements[key]] = value
            else:
                after[key] = value
        logger.debug(f"replacing it with: {after}")
        settings.set([index], after)

def v2(settings, logger):
    """Migration from v2 to v3"""
    # There were fields listed in the "removed" const that become rules
    removed = ["initial_value", "auto_on_before_print", "auto_off_after_print", "auto_off_delay"]
    for index in ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]: # no references to constants
        before = settings.get([index]) # without defaults
        after = {}
        logger.debug(f"relay {index} stored settings: {before}")
        for key, value in before.items():
            if key not in removed:
                after[key] = value
        initial_value = before.get("initial_value")
        if initial_value is None:
            initial_value = index == "r4" # v2 default: true for r4
        auto_on_before_print = before.get("auto_on_before_print")
        if auto_on_before_print is None:
            auto_on_before_print = index in ["r1", "r3", "r4"] # v2 default, true for these ones
        auto_off_after_print = before.get("auto_off_after_print")
        if auto_off_after_print is None:
            auto_off_after_print = index in ["r1", "r3", "r4"] # v2 default, true for these ones
        after["rules"] = { # no references to constants
            "STARTUP": {
                "state": bool(initial_value),
                "delay": 0
            },
            "PRINTING_STARTED": {
                "state": True if bool(auto_on_before_print) else None,
                "delay": 0
            },
            "PRINTING_STOPPED": {
                "state": False if bool(auto_off_after_print) else None,
                "delay": int(before.get("auto_off_delay") or 0)
            }
        }
        logger.debug(f"replacing it with: {after}")
        settings.set([index], after)

# List of migration functions starting from v0->v1
migrators = [ v0, v1, v2 ]

def migrate(current: int, settings, logger):
    # Current version number corresponds to the list index to begin migrations from
    jobs = migrators[current::]
    for index, job in enumerate(jobs):
        logger.info(f"Migrating to settings v{current + index + 1}")
        job(settings, logger)
