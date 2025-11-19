from dataclasses import asdict, dataclass, fields


@dataclass
class User:
    id: int
    username: str
    password: str
    email: str
    avatar_url: str | None = None

    @property
    def representation(self) -> dict:
        return asdict(self)
    
    @classmethod
    def create(cls, user_data: dict) -> 'User':
        return User(
            id=None,
            username=user_data.get('username'),
            password=user_data.get('password'),
            email=user_data.get('email'),
            avatar_url=None,
        )

    def set_password(self, hashed_password: str) -> None:
        self.password = hashed_password
