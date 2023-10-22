# -*- coding: utf-8 -*-
from typing import List
# todo after dropping 3.7 take TypedDict from typing instead
from typing_extensions import TypedDict


class Element(TypedDict):
    id: str
    name: str
    status: bool

Listing = List[Element]
