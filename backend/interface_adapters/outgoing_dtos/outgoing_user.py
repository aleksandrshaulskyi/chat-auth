from dataclasses import dataclass

from interface_adapters.shared_utils import add_from_dict


@dataclass
@add_from_dict
class OutgoingUserDTO:
    id: int
    username: str
    avatar_url: str
