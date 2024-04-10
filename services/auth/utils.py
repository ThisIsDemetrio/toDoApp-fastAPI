from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from app.Client import Client
from app.get_context import Context
from models.Token import Token, TokenData
from models.User import User, UserInDB
from app.auth import oauth2_scheme

# TODO: I'm confident this has to get out from here, and stored as an environment variable
# to get a string like this run: "openssl rand -hex 32!"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_user(client: Client, username: str):
    result = client.get_users_collection().find_one({'username': username})
    if result is not None:
        return UserInDB(**result)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_token(username: str) -> Token:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + access_token_expires
    }

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=access_token, token_type="bearer")

async def get_current_user(ctx: Context, token: Annotated[str, Depends(oauth2_scheme)]):
    logger = ctx.get('logger')
    client: Client = ctx.get('client')

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning(f'Unauthorized login for username {username}: username not found.')
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        logger.warning(f'Unauthorized login for username {username}: JWT error.')
        raise credentials_exception
    
    user = get_user(client, username=token_data.username)
    if user is None:
        logger.warning(f'Unauthorized login for username {username}: username not found.')
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    '''
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
    '''
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
