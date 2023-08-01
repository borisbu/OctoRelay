# -*- coding: utf-8 -*-
from typing import Optional
from RPi import GPIO

def xor(left: bool, right: bool) -> bool:
    return left is not right

class Relay():
    def __init__(self, pin: int, inverted: bool):
        self.pin = pin # GPIO pin
        self.inverted = inverted # marks the relay as normally closed

    def __repr__(self) -> str:
        return f"{type(self).__name__}(pin={self.pin},inverted={self.inverted})"

    def close(self):
        """Activates the current flow through the relay."""
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, xor(self.inverted, True))
        GPIO.setwarnings(True)

    def open(self):
        """Deactivates the current flow through the relay."""
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, xor(self.inverted, False))
        GPIO.setwarnings(True)

    def get_pin_state(self) -> bool:
        """Returns the logical state of the pin controlling the relay."""
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        state = bool(GPIO.input(self.pin))
        GPIO.setwarnings(True)
        return state

    def is_closed(self) -> bool:
        """Returns the logical state of the relay."""
        return xor(self.inverted, self.get_pin_state())

    def toggle(self, state: Optional[bool] = None) -> bool:
        """
        Switches the relay state to the one specified as an optional argument.
        If the argument is not specified then switches based on the current state.
        Returns the new logic state of the relay.
        """
        if state is None:
            state = not self.is_closed()
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, xor(self.inverted, state))
        GPIO.setwarnings(True)
        return state
