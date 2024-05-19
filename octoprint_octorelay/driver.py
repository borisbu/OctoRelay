# -*- coding: utf-8 -*-
from typing import Optional
from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value

class Relay():
    def __init__(self, pin: int, inverted: bool):
        self.request = request_lines(
            "/dev/gpiochip0",
            consumer = "OctoRelay",
            config = {
                pin: LineSettings(direction = Direction.OUTPUT, active_low = inverted)
            }
        )
        self.pin = pin # GPIO pin
        self.inverted = inverted # for serialization purposes only

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
        pin_state = self.request.get_value(self.pin) == Value.ACTIVE
        return pin_state

    def toggle(self, desired_state: Optional[bool] = None) -> bool:
        """
        Switches the relay state to the desired one specified as an optional argument.
        If the argument is not specified then switches based on the current state.
        Returns the new logical state of the relay.
        """
        if desired_state is None:
            desired_state = not self.is_closed()
        self.request.set_value(self.pin, Value.ACTIVE if desired_state else Value.INACTIVE)
        return desired_state
