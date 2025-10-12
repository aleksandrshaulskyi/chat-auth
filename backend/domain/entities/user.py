from dataclasses import dataclass, fields


@dataclass
class User:
    id: int
    username: str
    password: str
    email: str
    avatar_url: str | None = None

    def set_password(self, hashed_password: str) -> None:
        self.password = hashed_password

    def repr_without_none(self) -> dict:
        return {field.name: getattr(self, field.name) for field in fields(self)}
