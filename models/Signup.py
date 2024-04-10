from pydantic import BaseModel

class Signup(BaseModel):
    """Base model for a new user"""
    username: str
    email: str | None = None
    password: str