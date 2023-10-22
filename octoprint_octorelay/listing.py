# -*- coding: utf-8 -*-
from typing import List
# todo after dropping 3.7 take TypedDict from typing instead
from typing_extensions import TypedDict

# false positive, see https://github.com/pylint-dev/pylint/issues/4166
# pylint: disable=too-many-ancestors
# pylint: disable=too-few-public-methods
class Element(TypedDict):
    id: str
    name: str
    status: bool

Listing = List[Element]
