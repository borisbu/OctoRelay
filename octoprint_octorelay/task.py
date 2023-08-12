# -*- coding: utf-8 -*-
from octoprint.util import ResettableTimer
import time

class Task():
    def __init__(self, subject: str, target: bool, owner: str, delay: int, function, args):
        self.subject = subject
        self.target = target
        self.owner = owner
        self.delay = delay
        self.deadline = time.time() + delay
        # https://github.com/OctoPrint/OctoPrint/blob/ed4a264/src/octoprint/util/__init__.py#L1319
        self.timer = ResettableTimer(delay, function, args)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.subject},{self.target},{self.owner},{self.delay})"