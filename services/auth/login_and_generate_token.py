from app.get_context import Context
from models.Token import Token
from services.auth.utils import generate_token, get_user


def login_and_generate_token(ctx: Context, username: str, password: str) -> Token | None:
    pwd_context = ctx.get('pwd_context')
    client = ctx.get('client')
    logger = ctx.get('logger')

    user = get_user(client, username)
    if not user:
        logger.warning(f'Username {username} not found in database')
        return None
    if not pwd_context.verify(password, user.hashed_password):
        logger.warning(f'Username {username} found on database but password is not valid')
        return None
    
    return generate_token(ctx, username)