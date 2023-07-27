from octoprint.access import ADMIN_GROUP, USER_GROUP

# Plugin's default settings
defaultSettings = {
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
relayIndexes = defaultSettings.keys()

# Plugin's template
templates = [
    { "type": "navbar", "custom_bindings": False },
    { "type": "settings", "custom_bindings": False }
]

# Plugin's asset files to automatically include in the core UI
assets = { "js": [ "js/octorelay.js" ] }

# Accepted commands with their lists of mandatory parameters
apiCommands = {
    "update": [ "pin" ],
    "getStatus": [ "pin" ],
    "listAllStatus": [],
}

# see https://docs.octoprint.org/en/master/plugins/hooks.html#octoprint-access-permissions
permissions = [{
    "key": "SWITCH",
    "name": "Relay switching",
    "description": "Allows to switch GPIO pins and execute related OS commands.",
    "roles": [ "switch" ],
    "dangerous": False,
    "default_groups": [ ADMIN_GROUP, USER_GROUP ]
}]
