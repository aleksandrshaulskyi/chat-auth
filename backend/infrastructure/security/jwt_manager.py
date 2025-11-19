from datetime import datetime, timedelta, timezone

from jwt import encode, decode, PyJWTError

from application.exceptions import AuthenticationException
from application.ports.jwt_manager import JWTManagerPort

from settings import settings


class JWTManager(JWTManagerPort):

    async def issue_pair(self, user_id: int) -> dict:
        access_token_exp_time = datetime.now(timezone.utc) + timedelta(minutes=720)
        refresh_token_exp_time = datetime.now(timezone.utc) + timedelta(minutes=1440)

        access_token = await self.issue_token(expiration_time=access_token_exp_time, user_id=user_id)
        refresh_token = await self.issue_token(expiration_time=refresh_token_exp_time, user_id=user_id)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

    async def issue_token(self, expiration_time: timedelta, user_id: int) -> str:
        payload = {'exp': expiration_time, 'user_id': user_id}
        return encode(payload=payload, key=settings.key, algorithm=settings.algorithm)

    async def verify(self, token: str) -> bool:
        try:
            decode(jwt=token, key=settings.key, algorithms=[settings.algorithm])
        except PyJWTError:
            raise AuthenticationException(
                title='Authentication exception.',
                details={'Authentication exception.': 'Invalid JWT was provided.'},
            )
        
    async def get_user_id(self, token: str) -> str | None:
        try:
            payload = decode(jwt=token, key=settings.key, algorithms=[settings.algorithm])
        except PyJWTError:
            raise AuthenticationException(
                title='Authentication exception.',
                details={'Authentication exception.': 'Invalid JWT was provided.'},
            )
        else:
            if (user_id := payload.get('user_id')) is not None:
                return user_id
            raise AuthenticationException(
                title='Authentication exception.',
                details={'Authentication exception.': 'Invalid JWT payload.'},
            )
