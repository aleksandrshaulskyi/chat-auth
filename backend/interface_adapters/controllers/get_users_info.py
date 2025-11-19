from application.ports import UserRepositoryPort
from application.use_cases import GetUsersInfoUseCase
from interface_adapters.outgoing_dtos import OutgoingUserDTO


class GetUsersInfoController:
    """
    The controller that is responsible for retrieving the information about users
    based on their ids.
    """

    def __init__(self, user_ids: dict, database_repo: UserRepositoryPort) -> None:
        """
        Initialize the controller.

        Args:
            user_ids (list): A list of ids of the users that should be found.
            database_repo (UserRepositoryPort): The port responsible for actions with users.
        """
        self.user_ids = user_ids
        self.database_repo = database_repo

    async def get_users_info(self) -> list:
        """
        Get users information.
        """
        user_ids = self.user_ids.get('user_ids')

        raw_users = await GetUsersInfoUseCase(
            user_ids=user_ids,
            database_repo=self.database_repo,
        ).execute()
        
        clean_users = [OutgoingUserDTO.from_dict(raw_user) for raw_user in raw_users]

        return clean_users
