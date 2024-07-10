# -*- coding: utf-8 -*-
from typing import Optional, List
from gpiozero import LED

def xor(left: bool, right: bool) -> bool:
    return left is not right

class Driver():
    cache: List["Driver"] = []

    def __init__(self, pin: int, inverted: bool, pin_factory=None):
        self.pin = pin # GPIO pin
        self.inverted = inverted # marks the relay as normally closed
        self.handle = LED(pin, pin_factory=pin_factory)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(pin={self.pin},inverted={self.inverted},closed={self.is_closed()})"

    def close(self):
        """Activates the current flow through the relay."""
        self.toggle(True)

    def open(self):
        """Deactivates the current flow through the relay."""
        self.toggle(False)

    def is_closed(self) -> bool:
        """Returns the logical state of the relay."""
        return xor(self.inverted, self.handle.is_lit)

    def toggle(self, desired_state: Optional[bool] = None) -> bool:
        """
        Switches the relay state to the desired one specified as an optional argument.
        If the argument is not specified then switches based on the current state.
        Returns the new logical state of the relay.
        """
        if desired_state is None:
            desired_state = not self.is_closed()
        (self.handle.on if xor(self.inverted, desired_state) else self.handle.off)()
        return desired_state

    @classmethod
    def ensure(cls, pin: int, inverted: bool, pin_factory=None):
        for relay in cls.cache:
            if relay.pin == pin:
                if xor(relay.inverted, inverted):
                    relay.inverted = inverted
                return relay
        relay = cls(pin, inverted, pin_factory)
        cls.cache.append(relay)
        return relay
