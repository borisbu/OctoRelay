# -*- coding: utf-8 -*-
from typing import Optional
from RPi import GPIO

# The driver operated BCM mode of pins enumeration
GPIO.setmode(GPIO.BCM)

def xor(left: bool, right: bool) -> bool:
    return left is not right

class Relay():
    def __init__(self, pin: int, inverted: bool):
        self.pin = pin # GPIO pin
        self.inverted = inverted # marks the relay as normally closed, None - when only going to read its pin state

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
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        pin_state = bool(GPIO.input(self.pin))
        GPIO.setwarnings(True)
        return xor(self.inverted, pin_state)

    def toggle(self, desired_state: Optional[bool] = None) -> bool:
        """
        Switches the relay state to the desired one specified as an optional argument.
        If the argument is not specified then switches based on the current state.
        Returns the new logical state of the relay.
        """
        if desired_state is None:
            desired_state = not self.is_closed()
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, xor(self.inverted, desired_state))
        GPIO.setwarnings(True)
        return desired_state
