# -*- coding: utf-8 -*-
from octoprint.access import ADMIN_GROUP, USER_GROUP

# Internal events
STARTUP = "STARTUP"
PRINTING_STARTED = "PRINTING_STARTED"
PRINTING_STOPPED = "PRINTING_STOPPED"
TURNED_ON = "TURNED_ON"
USER_ACTION = "USER_ACTION"

# Task cancellation exceptions
# { eventHappened: [ events which postponed timers should NOT be cancelled ]
CANCELLATION_EXCEPTIONS = {}
# min seconds before the task can be cancelled
PREEMPTIVE_CANCELLATION_CUTOFF = 2

# Versioning of the plugin's default settings described below
SETTINGS_VERSION = 3

# Plugin's default settings, immutable getter
# Warning: every amendment or deletion of these settings requires:
# - to increase the SETTINGS_VERSION above
# - and migration to preserve user's previous configuration intact
def get_default_settings():
    return {
        "r1": {
            "active": False,
            "relay_pin": 4,
            "inverted_output": True,
            "cmd_on": "",
            "cmd_off": "",
            "icon_on": "&#128161;",
            "icon_off": """<div style="filter: grayscale(90%)">&#128161;</div>""",
            "label_text": "Light",
            "confirm_off": False,
            "show_upcoming": True,
            "rules": {
                STARTUP: {
                    "state": False,
                    "delay": 0,
                },
                PRINTING_STARTED: {
                    "state": True,
                    "delay": 0,
                },
                PRINTING_STOPPED: {
                    "state": False,
                    "delay": 10,
                },
                TURNED_ON: {
                    "state": None,
                    "delay": 0
                }
            },
        },
        "r2": {
            "active": False,
            "relay_pin": 17,
            "inverted_output": True,
            "cmd_on": "",
            "cmd_off": "",
            "icon_on": """<img width="24" height="24" src="/plugin/octorelay/static/img/3d-printer.svg">""",
            "icon_off": (
                """<img width="24" height="24" src="/plugin/octorelay/static/img/3d-printer.svg" """
                """style="filter: opacity(20%)">"""
            ),
            "label_text": "Printer",
            "confirm_off": True,
            "show_upcoming": True,
            "rules": {
                STARTUP: {
                    "state": False,
                    "delay": 0,
                },
                PRINTING_STARTED: {
                    "state": None,
                    "delay": 0,
                },
                PRINTING_STOPPED: {
                    "state": None,
                    "delay": 0,
                },
                TURNED_ON: {
                    "state": None,
                    "delay": 0
                }
            },
        },
        "r3": {
            "active": False,
            "relay_pin": 18,
            "inverted_output": True,
            "cmd_on": "",
            "cmd_off": "",
            "icon_on": """<img width="24" height="24" src="/plugin/octorelay/static/img/fan.svg" >""",
            "icon_off": (
                """<img width="24" height="24" src="/plugin/octorelay/static/img/fan.svg" """
                """style="filter: opacity(20%)">"""
            ),
            "label_text": "Fan",
            "confirm_off": False,
            "show_upcoming": True,
            "rules": {
                STARTUP: {
                    "state": False,
                    "delay": 0,
                },
                PRINTING_STARTED: {
                    "state": True,
                    "delay": 0,
                },
                PRINTING_STOPPED: {
                    "state": False,
                    "delay": 10,
                },
                TURNED_ON: {
                    "state": None,
                    "delay": 0
                }
            },
        },
        "r4": {
            "active": False,
            "relay_pin": 23,
            "inverted_output": True,
            "cmd_on": "sudo service webcamd start",
            "cmd_off": "sudo service webcamd stop",
            "icon_on": """<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" >""",
            "icon_off": (
                """<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" """
                """style="filter: opacity(20%)">"""
            ),
            "label_text": "Webcam",
            "confirm_off": False,
            "show_upcoming": True,
            "rules": {
                STARTUP: {
                    "state": True,
                    "delay": 0,
                },
                PRINTING_STARTED: {
                    "state": True,
                    "delay": 0,
                },
                PRINTING_STOPPED: {
                    "state": False,
                    "delay": 10,
                },
                TURNED_ON: {
                    "state": None,
                    "delay": 0
                }
            },
        },
        "r5": {
            "active": False,
            "relay_pin": 24,
            "inverted_output": True,
            "cmd_on": "",
            "cmd_off": "",
            "icon_on": "ON",
            "icon_off": "OFF",
            "label_text": "R5",
            "confirm_off": False,
            "show_upcoming": True,
            "rules": {
                STARTUP: {
                    "state": False,
                    "delay": 0,
                },
                PRINTING_STARTED: {
                    "state": None,
                    "delay": 0,
                },
                PRINTING_STOPPED: {
                    "state": None,
                    "delay": 0,
                },
                TURNED_ON: {
                    "state": None,
                    "delay": 0
                }
            },
        },
        "r6": {
            "active": False,
            "relay_pin": 25,
            "inverted_output": True,
            "cmd_on": "",
            "cmd_off": "",
            "icon_on": "&#128161;",
            "icon_off": """<div style="filter: grayscale(90%)">&#128161;</div>""",
            "label_text": "R6",
            "confirm_off": False,
            "show_upcoming": True,
            "rules": {
                STARTUP: {
                    "state": False,
                    "delay": 0,
                },
                PRINTING_STARTED: {
                    "state": None,
                    "delay": 0,
                },
                PRINTING_STOPPED: {
                    "state": None,
                    "delay": 0,
                },
                TURNED_ON: {
                    "state": None,
                    "delay": 0
                }
            },
        },
        "r7": {
            "active": False,
            "relay_pin": 8,
            "inverted_output": True,
            "cmd_on": "",
            "cmd_off": "",
            "icon_on": "&#128161;",
            "icon_off": """<div style="filter: grayscale(90%)">&#128161;</div>""",
            "label_text": "R7",
            "confirm_off": False,
            "show_upcoming": True,
            "rules": {
                STARTUP: {
                    "state": False,
                    "delay": 0,
                },
                PRINTING_STARTED: {
                    "state": None,
                    "delay": 0,
                },
                PRINTING_STOPPED: {
                    "state": None,
                    "delay": 0,
                },
                TURNED_ON: {
                    "state": None,
                    "delay": 0
                }
            },
        },
        "r8": {
            "active": False,
            "relay_pin": 7,
            "inverted_output": True,
            "cmd_on": "",
            "cmd_off": "",
            "icon_on": "&#128161;",
            "icon_off": """<div style="filter: grayscale(90%)">&#128161;</div>""",
            "label_text": "R8",
            "confirm_off": False,
            "show_upcoming": True,
            "rules": {
                STARTUP: {
                    "state": False,
                    "delay": 0,
                },
                PRINTING_STARTED: {
                    "state": None,
                    "delay": 0,
                },
                PRINTING_STOPPED: {
                    "state": None,
                    "delay": 0,
                },
                TURNED_ON: {
                    "state": None,
                    "delay": 0
                }
            },
        },
    }

# Keys of the default settings, used for iterations: [r1...r8]
RELAY_INDEXES = get_default_settings().keys()

# Plugin templates, immutable getter
def get_templates():
    return [
        { "type": "navbar", "custom_bindings": False },
        { "type": "settings", "custom_bindings": False }
    ]

# these are available in templates with prefix: plugin_octorelay_
def get_ui_vars():
    return {
        "events": {
            STARTUP: { "label": "on Startup", "disabled": [] },
            PRINTING_STARTED: { "label": "on Printing Started", "disabled": [] },
            PRINTING_STOPPED: { "label": "on Printing Stopped", "disabled": [] },
            TURNED_ON: { "label": "after Turned ON", "disabled": [ "true" ] }
        },
        "boolean": {
            "true": { "caption": "YES", "color": "info" },
            "false": { "caption": "NO", "color": "default" }
        },
        "tristate": {
            "true": { "caption": "ON", "color": "success" },
            "null": { "caption": "skip", "color": "default" },
            "false": { "caption": "OFF", "color": "danger" }
        }
    }

# Plugin's asset files to automatically include in the core UI
ASSETS = {
    "js": [ "js/octorelay.js" ],
    "css": [ "css/octorelay.css" ]
}

# Public interface commands:
UPDATE_COMMAND = "update"
GET_STATUS_COMMAND = "getStatus"
LIST_ALL_COMMAND = "listAllStatus"
CANCEL_TASK_COMMAND = "cancelTask"
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
