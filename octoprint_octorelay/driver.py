# -*- coding: utf-8 -*-
from RPi import GPIO

def xor(left: bool, right: bool):
    return left is not right

class Relay():
    def __init__(self, inverted: bool, pin: int):
        self.inverted = inverted # marks the relay as normally closed
        self.pin = pin # GPIO pin

    def __repr__(self) -> str:
        return f"{type(self).__name__}(pin={self.pin},inverted={self.inverted})"

    def close(self):
        """Activates the current flow through the relay"""
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, xor(self.inverted, True))
        GPIO.setwarnings(True)

    def open(self):
        """Deactivates the current flow through the relay"""
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, xor(self.inverted, False))
        GPIO.setwarnings(True)

    def get_pin_state(self) -> bool:
        """Returns the logical state of the pin controlling the relay"""
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        state = bool(GPIO.input(self.pin))
        GPIO.setwarnings(True)
        return state

    def is_closed(self) -> bool:
        """Returns the logical state of the relay"""
        return xor(self.inverted, self.get_pin_state())

    def toggle(self):
        """Switches the relay state"""
        state = not self.is_closed()
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, xor(self.inverted, state))
        GPIO.setwarnings(True)
