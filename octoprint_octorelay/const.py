from octoprint.access import ADMIN_GROUP, USER_GROUP

# Plugin's default settings
DEFAULT_SETTINGS = {
    "r1": {
        "active": True,
        "relay_pin": 4,
        "inverted_output": True,
        "initial_value": False,
        "cmdON": "",
        "cmdOFF": "",
        "iconOn": "&#128161;",
        "iconOff": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
        "labelText": "Light",
        "confirmOff": False,
        "autoONforPrint": True,
        "autoOFFforPrint": True,
        "autoOffDelay": 10,
    },
    "r2": {
        "active": True,
        "relay_pin": 17,
        "inverted_output": True,
        "initial_value": False,
        "cmdON": "",
        "cmdOFF": "",
        "iconOn": """<img width="24" height="24" src="/plugin/octorelay/static/img/3d-printer.svg">""",
        "iconOff": """<img width="24" height="24" src="/plugin/octorelay/static/img/3d-printer.svg" style="filter: opacity(20%)">""",
        "labelText": "Printer",
        "confirmOff": True,
        "autoONforPrint": False,
        "autoOFFforPrint": False,
        "autoOffDelay": 0,
    },
    "r3": {
        "active": True,
        "relay_pin": 18,
        "inverted_output": True,
        "initial_value": False,
        "cmdON": "",
        "cmdOFF": "",
        "iconOn": """<img width="24" height="24" src="/plugin/octorelay/static/img/fan.svg" >""",
        "iconOff": """<img width="24" height="24" src="/plugin/octorelay/static/img/fan.svg" style="filter: opacity(20%)">""",
        "labelText": "Fan",
        "confirmOff": False,
        "autoONforPrint": True,
        "autoOFFforPrint": True,
        "autoOffDelay": 10,
    },
    "r4": {
        "active": True,
        "relay_pin": 23,
        "inverted_output": True,
        "initial_value": True,
        "cmdON": "sudo service webcamd start",
        "cmdOFF": "sudo service webcamd stop",
        "iconOn": """<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" >""",
        "iconOff": """<img width="24" height="24" src="/plugin/octorelay/static/img/webcam.svg" style="filter: opacity(20%)">""",
        "labelText": "Webcam",
        "confirmOff": False,
        "autoONforPrint": True,
        "autoOFFforPrint": True,
        "autoOffDelay": 10,
    },
    "r5": {
        "active": False,
        "relay_pin": 24,
        "inverted_output": True,
        "initial_value": False,
        "cmdON": "",
        "cmdOFF": "",
        "iconOn": "ON",
        "iconOff": "OFF",
        "labelText": "R5",
        "confirmOff": False,
        "autoONforPrint": False,
        "autoOFFforPrint": False,
        "autoOffDelay": 0,
    },
    "r6": {
        "active": False,
        "relay_pin": 25,
        "inverted_output": True,
        "initial_value": False,
        "cmdON": "",
        "cmdOFF": "",
        "iconOn": "&#128161;",
        "iconOff": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
        "labelText": "R6",
        "confirmOff": False,
        "autoONforPrint": False,
        "autoOFFforPrint": False,
        "autoOffDelay": 0,
    },
    "r7": {
        "active": False,
        "relay_pin": 8,
        "inverted_output": True,
        "initial_value": False,
        "cmdON": "",
        "cmdOFF": "",
        "iconOn": "&#128161;",
        "iconOff": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
        "labelText": "R7",
        "confirmOff": False,
        "autoONforPrint": False,
        "autoOFFforPrint": False,
        "autoOffDelay": 0,
    },
    "r8": {
        "active": False,
        "relay_pin": 7,
        "inverted_output": True,
        "initial_value": False,
        "cmdON": "",
        "cmdOFF": "",
        "iconOn": "&#128161;",
        "iconOff": "<div style=\"filter: grayscale(90%)\">&#128161;</div>",
        "labelText": "R8",
        "confirmOff": False,
        "autoONforPrint": False,
        "autoOFFforPrint": False,
        "autoOffDelay": 0,
    },
}

# Keys of the default settings, used for iterations: [r1...r8]
RELAY_INDEXES = DEFAULT_SETTINGS.keys()

# Plugin's templates
TEMPLATES = [
    { "type": "navbar", "custom_bindings": False },
    { "type": "settings", "custom_bindings": False }
]

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
    "pip": f"https://github.com/{GITHUB['user']}/{GITHUB['repo']}/archive/{{target}}.zip",
    "stable_branch": STABLE_CHANNEL,
    "prerelease_branches": [ PRE_RELEASE_CHANNEL ]
}

POLLING_INTERVAL = 0.3
