from dataclasses import dataclass

from interfaces.shared_utils import add_from_dict


@dataclass
@add_from_dict
class UserOut:
    id: int
    username: str
    email: str
    avatar_url: str
