# -*- coding: utf-8 -*-
def migrate(current: int, settings, logger):
    # List of migration functions beginning from the one needed to migrate from v0 to v1
    migrations = [ to_v1 ]
    # Current version number corresponds to the list index to begin migrations from
    jobs = migrations[current::]
    for job in jobs:
        job(settings, logger)

def to_v1(settings, logger):
    # First 4 relays used to have active=True
    logger.info("OctoRelay migrates to settings v1")
    for index in ["r1", "r2", "r3", "r4"]:
        stored = settings.get([index])
        logger.debug(f"relay {index} stored settings: {stored}")
        if "active" not in stored:
            logger.debug("inserting active=True into it")
            override = { **stored, "active": True }
            settings.set([index], override)
