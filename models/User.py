from pydantic import BaseModel


def validate_role(value):
    if value not in ["admin", "user"]:
        raise ValueError(f"Role must be either 'admin' or 'user', not {value}")
    return value


class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None
    role: str

    @classmethod
    def __get_validators__(cls):
        yield validate_role


class UserInDB(User):
    hashed_password: str
