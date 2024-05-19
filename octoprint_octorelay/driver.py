# -*- coding: utf-8 -*-
from typing import Optional
import gpiod

def xor(left: bool, right: bool) -> bool:
    return left is not right

class Relay():
    def __init__(self, pin: int, inverted: bool):
        self.path = "/dev/gpiochip0"
        self.pin = pin # GPIO pin
        self.inverted = inverted # marks the relay as normally closed

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
        request = gpiod.request_lines(
            self.path,
            consumer = "OctoRelay",
            config = {
                self.pin: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)
            }
        )
        pin_state = request.get_value(self.pin) == gpiod.line.Value.ACTIVE
        return xor(self.inverted, pin_state)

    def toggle(self, desired_state: Optional[bool] = None) -> bool:
        """
        Switches the relay state to the desired one specified as an optional argument.
        If the argument is not specified then switches based on the current state.
        Returns the new logical state of the relay.
        """
        if desired_state is None:
            desired_state = not self.is_closed()
        request = gpiod.request_lines(
            self.path,
            consumer = "OctoRelay",
            config = {
                self.pin: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)
            }
        )
        request.set_value(self.pin, gpiod.line.Value.ACTIVE if xor(self.inverted, desired_state) else gpiod.line.Value.INACTIVE)
        return desired_state
