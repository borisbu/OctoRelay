# -*- coding: utf-8 -*-
def v0(settings, logger):
    """Migration from v0 to v1"""
    # First 4 relays used to have active=True
    for index in ["r1", "r2", "r3", "r4"]:
        before = settings.get([index])
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
    for index in ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]:
        before = settings.get([index])
        after = {}
        logger.debug(f"relay {index} stored settings: {before}")
        for key, value in before.items():
            if key in replacements:
                after[replacements[key]] = value
            else:
                after[key] = value
        logger.debug(f"replacing it with: {after}")
        settings.set([index], after)

# List of migration functions starting from v0->v1
migrators = [ v0, v1 ]

def migrate(current: int, settings, logger):
    # Current version number corresponds to the list index to begin migrations from
    jobs = migrators[current::]
    for index, job in enumerate(jobs):
        logger.info(f"OctoRelay migrates to settings v{index + 1}")
        job(settings, logger)
