# -*- coding: utf-8 -*-
from typing import Optional
from gpiozero import LED


relays = []


def xor(left: bool, right: bool) -> bool:
    return left is not right


class Relay():
    def __init__(self, pin: int, inverted: bool):
        self.pin = pin # GPIO pin
        self.inverted = inverted # marks the relay as normally closed
        self.relay = LED(pin)

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
        return xor(self.inverted, self.relay.is_lit)

    def toggle(self, desired_state: Optional[bool] = None) -> bool:
        """
        Switches the relay state to the desired one specified as an optional argument.
        If the argument is not specified then switches based on the current state.
        Returns the new logical state of the relay.
        """
        if desired_state is None:
            desired_state = not self.is_closed()
        
        if xor(self.inverted, desired_state) is True:
            self.relay.on()
        else:
            self.relay.off()

        return desired_state


def get_or_create_relay(pin: int, inverted: bool):
    to_return = None

    for relay in relays:
        if relay.pin == pin:
            if relay.inverted != inverted:
                relay.inverted = inverted

            to_return = relay
            break

    if to_return is None:
        relay = Relay(pin, inverted)
        relays.append(relay)
        to_return = relay

    return to_return
