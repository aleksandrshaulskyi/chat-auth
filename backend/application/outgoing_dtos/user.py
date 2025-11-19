from dataclasses import asdict, dataclass


@dataclass
class OutgoingUserDTO:
    """
    This dataclass is used for the transmission of User data
    between microservices.
    """
    id: int
    username: str
    avatar_url: str

    @property
    def representation(self) -> dict:
        """
        Get dataclass representation.

        Returns:
            dict: Serializable representation of OutgoingUserDTO.
        """
        return asdict(self)

    @classmethod
    def create(cls, user_data: dict) -> 'OutgoingUserDTO':
        """
        Safely create an instance of the dataclass.

        Returns:
            OutgoingUserDTO: An instance of OutgoingUserDTO.
        """
        return OutgoingUserDTO(
            id=user_data.get('id'),
            username=user_data.get('username'),
            avatar_url=user_data.get('avatar_url'),
        )
