# -*- coding: utf-8 -*-
from octoprint.access import ADMIN_GROUP, USER_GROUP

# Keys of the default settings, used for iterations: [r1...r8]
RELAY_INDEXES = ["r1", "r2", "r3" , "r4", "r5", "r6", "r7", "r8"]

# Plugin's asset files to automatically include in the core UI
ASSETS = { "js": [ "js/octorelay.js" ] }

# Public interface commands:
UPDATE_COMMAND = "update"
GET_STATUS_COMMAND = "getStatus"
LIST_ALL_COMMAND = "listAllStatus"
AT_COMMAND = "OCTORELAY"

# see https://docs.octoprint.org/en/master/plugins/hooks.html#octoprint-access-permissions
SWITCH_PERMISSION = {
    "key": "SWITCH",
    "name": "Relay switching",
    "description": "Allows to switch GPIO pins and execute related OS commands.",
    "roles": [ "switch" ],
    "dangerous": False,
    "default_groups": [ ADMIN_GROUP, USER_GROUP ]
}

# used by UPDATES_CONFIG
GITHUB = {
    "user": "borisbu",
    "repo": "OctoRelay"
}

# used by UPDATES_CONFIG
STABLE_CHANNEL = {
    "name": "Stable",
    "branch": "master",
    "commitish": [ "master" ]
}

# used by UPDATES_CONFIG
PRE_RELEASE_CHANNEL = {
    "name": "Prerelease",
    "branch": "develop",
    "commitish": [ "develop", "master" ]
}

# https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html#octoprint-plugin-softwareupdate-check-config
UPDATES_CONFIG = {
    **GITHUB,
    "type": "github_release",
    "pip": f"https://github.com/{GITHUB['user']}/{GITHUB['repo']}/releases/download/{{target}}/release.zip",
    "stable_branch": STABLE_CHANNEL,
    "prerelease_branches": [ PRE_RELEASE_CHANNEL ]
}

POLLING_INTERVAL = 0.3
