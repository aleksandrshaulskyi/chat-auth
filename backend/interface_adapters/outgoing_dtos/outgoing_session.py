from dataclasses import dataclass

from interface_adapters.shared_utils import add_from_dict

@dataclass
@add_from_dict
class OutgoingSessionDTO:
    """
    This DTO is used to adapt the internal Session representation to
    the outgoing format.
    """
    access_token: str
    refresh_token: str
