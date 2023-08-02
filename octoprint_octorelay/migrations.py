# -*- coding: utf-8 -*-
def migrate(current: int, settings, logger):
    if current < 1:
        migrate_to_v1(settings, logger)

def migrate_to_v1(settings, logger):
    # First 4 relays used to have active=True
    logger.info("OctoRelay migrates to settings v1")
    for index in ["r1", "r2", "r3", "r4"]:
        stored = settings.get([index])
        logger.debug(f"relay {index} stored settings: {stored}")
        if "active" not in stored:
            logger.debug("inserting active=True into it")
            override = { **stored, "active": True }
            settings.set([index], override)
