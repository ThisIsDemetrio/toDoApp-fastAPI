from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None
    # TODO: This should be either "admin" or "user", can we enforce that?
    role: str

class UserInDB(User):
    hashed_password: str