from application.exceptions import AuthenticationException, InvalidJWTException
from application.ports import JWTTokenProviderPort, UserRepositoryPort
from domain.entities import User


class GetUserUseCase:

    def __init__(
        self,
        access_token: str,
        database_repo: UserRepositoryPort,
        jwt_provider: JWTTokenProviderPort,
    ) -> None:
        self.access_token = access_token
        self.database_repo = database_repo
        self.jwt_provider = jwt_provider

    async def execute(self) -> User | None:
        user_id = await self.get_user_id()

        if (user_data := await self.database_repo.get_by_id(id=user_id)) is not None:
            return User(**user_data)
        exception_details = {
            'details': {'non-field-error': 'The user does not exist.'}
        }
        raise AuthenticationException(details=exception_details)

    async def get_user_id(self) -> str | None:
        try:
            return await self.jwt_provider.get_user_id(token=self.access_token)
        except InvalidJWTException:
            exception_details = {
                'details': {'non-field-error': 'An invalid JWT token provided.'}
            }
            raise AuthenticationException(details=exception_details)
