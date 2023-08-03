# -*- coding: utf-8 -*-
def v0(settings, logger):
    """Migration from v0 to v1"""
    # First 4 relays used to have active=True
    for index in ["r1", "r2", "r3", "r4"]:
        stored = settings.get([index])
        logger.debug(f"relay {index} stored settings: {stored}")
        if "active" not in stored:
            logger.debug("inserting active=True into it")
            override = { **stored, "active": True }
            settings.set([index], override)

# List of migration functions starting from v0->v1
migrators = [ v0 ]

def migrate(current: int, settings, logger):
    # Current version number corresponds to the list index to begin migrations from
    jobs = migrators[current::]
    for index, job in enumerate(jobs):
        logger.info(f"OctoRelay migrates to settings v{index + 1}")
        job(settings, logger)
