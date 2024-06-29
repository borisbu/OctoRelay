# -*- coding: utf-8 -*-
from typing import Optional
from gpiozero import LED


relays = []


class Relay():
    def __init__(self, pin: int, inverted: bool):
        self.pin = pin # GPIO pin
        self.inverted = inverted # marks the relay as normally closed
        self.relay = LED(pin, active_high=inverted)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(pin={self.pin},inverted={self.inverted},closed={self.is_closed()})"

    def close(self):
        """Activates the current flow through the relay."""
        self.relay.on()

    def open(self):
        """Deactivates the current flow through the relay."""
        self.relay.off()

    def is_closed(self) -> bool:
        """Returns the logical state of the relay."""
        return self.relay.is_lit

    def toggle(self, desired_state: Optional[bool] = None) -> bool:
        """
        Switches the relay state to the desired one specified as an optional argument.
        If the argument is not specified then switches based on the current state.
        Returns the new logical state of the relay.
        """
        self.relay.toggle()
        return desired_state


def get_or_create_relay(pin: int, inverted: bool):
    to_return = None

    for relay in relays:
        if relay.pin == pin:
            to_return = relay
            break

    if to_return is None:
        relay = Relay(pin, inverted)
        relays.append(relay)
        to_return = relay

    return to_return


if __name__ == '__main__':
    a = get_or_create_relay(15, True)
    print(a.is_closed())
    a.close()
    print(a.is_closed())

    a = get_or_create_relay(15, True)
    print(a.is_closed())