from app.Client import Client
from app.get_context import Context
from app.responses.UsernameAlreadyTaken import UsernameAlreadyTaken
from models import Signup
from passlib.context import CryptContext
from models.Token import Token
from services.auth.utils import generate_token, get_user


def get_password_hash(pwd_context, password):
    return pwd_context.hash(password)


def create_user_and_generate_token(
    ctx: Context, data: Signup
) -> Token | UsernameAlreadyTaken:
    pwd_context: CryptContext = ctx.get("pwd_context")
    client: Client = ctx.get("client")

    user = get_user(client, data.username)
    if user:
        return UsernameAlreadyTaken(data.username)

    client.get_users_collection().insert_one(
        {
            "username": data.username,
            "hashed_password": get_password_hash(pwd_context, data.password),
            "email": data.email,
            "disabled": False,
            "role": "user",
        }
    )

    return {"status": "OK", "token": generate_token(ctx, data.username)}
