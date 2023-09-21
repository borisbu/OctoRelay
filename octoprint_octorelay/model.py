from typing import Optional
# todo after dropping 3.7 replace with "from typing"
from typing_extensions import TypedDict

class UpcomingModel(TypedDict):
    target: bool
    owner: str
    deadline: int

class Model(TypedDict):
    relay_pin: int
    inverted_output: bool
    relay_state: bool
    label_text: str
    active: bool
    icon_html: str
    confirm_off: bool
    upcoming: Optional[UpcomingModel]
