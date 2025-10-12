from dataclasses import dataclass

from interfaces.shared_utils import add_from_dict

@dataclass
@add_from_dict
class SessionOut:
    access_token: str
    refresh_token: str
