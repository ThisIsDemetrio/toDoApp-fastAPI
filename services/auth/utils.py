from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from app.Client import Client
from app.Settings import Settings
from app.get_context import Context
from models.Token import Token, TokenData
from models.User import User, UserInDB
from app.auth import oauth2_scheme

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user(client: Client, username: str):
    result = client.get_users_collection().find_one({"username": username})
    if result is not None:
        return UserInDB(**result)


def generate_token(ctx: Context, username: str) -> Token:
    settings: Settings = ctx.get("settings")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + access_token_expires,
    }

    access_token = jwt.encode(to_encode, settings.hash_key, algorithm=ALGORITHM)
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(ctx: Context, token: Annotated[str, Depends(oauth2_scheme)]):
    logger = ctx.get("logger")
    client: Client = ctx.get("client")
    settings: Settings = ctx.get("settings")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.hash_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning(
                f"Unauthorized login for username {username}: username not found."
            )
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        logger.warning(f"Unauthorized login for username {username}: JWT error.")
        raise credentials_exception

    user = get_user(client, username=token_data.username)
    if user is None:
        logger.warning(
            f"Unauthorized login for username {username}: username not found."
        )
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Method that returns the current user, but that can be used as well to verify
    if the user is valid and has a token.

    Can be used as a dependency:
    ```
    router.get("/", response_model=..., dependencies=[Depends(get_current_active_user)])
    async def get(...):
    ```

    or in the parameters (to actually use the user instance):
    ```
    @router.get("/")
    async def get(current_user: Annotated[User, Depends(get_current_active_user)]):
    ```

    according to your needs.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
