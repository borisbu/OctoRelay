# -*- coding: utf-8 -*-
from typing import Optional, Dict
# todo after dropping 3.7 take TypedDict from typing instead
from typing_extensions import TypedDict

from .const import RELAY_INDEXES

# pylint: disable=too-few-public-methods

class Upcoming(TypedDict):
    target: bool
    owner: str
    deadline: int

class Entry(TypedDict):
    relay_pin: int
    inverted_output: bool
    relay_state: bool
    label_text: str
    active: bool
    icon_html: str
    confirm_off: bool
    upcoming: Optional[Upcoming]

Model = Dict[str, Entry]

def get_initial_model() -> Model:
    return {
        index: {
            "relay_pin": 0,
            "inverted_output": False,
            "relay_state": False,
            "label_text": index,
            "active": False,
            "icon_html": index,
            "confirm_off": False,
            "upcoming": None
        } for index in RELAY_INDEXES
    }
