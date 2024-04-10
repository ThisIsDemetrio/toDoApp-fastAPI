from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import error_handling
from app.get_context import Context
from app.auth import oauth2_scheme

from models.Signup import Signup
from models.User import User
from models.Token import Token
from services.auth.utils import get_password_hash, get_user, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user

# TODO: Add route to add users
# TODO: Move logic to services

# NOTE: I cannot use prefix because nested routes won't be found by oauth2_scheme. I guess I'll keep it that way 
router = APIRouter(tags=['Authentication'])

@router.post("/signup")
async def signup(ctx: Context, form_data: Signup) -> Token:
    # TODO: form_data should be an actual form_data, perhaps
    logger = ctx.get('logger')
    client = ctx.get('client')
    pwd_context = ctx.get('pwd_context')

    logger.debug(f'POST /signup with username "{form_data.username}" and password "{form_data.password}"')
    # TODO: We should check if username, password and email are valid and respect the validation rules, otherwise is 400

    user = get_user(client, form_data.username)
    if user:
        logger.warning(f'Username "{form_data.username}" already taken.')
        return error_handling.return_error(error_handling.Y00)

    try:
        client.get_users_collection().insert_one({
            "username": form_data.username,
            "hashed_password": get_password_hash(pwd_context, form_data.password),
            "email": form_data.email,
            "disabled": False,
            "role": "user"
        })
    except Exception as e:
        logger.error(f'POST /signup returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # TODO: investigate if generating this token should also give me authentication
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/login")
async def login(ctx: Context, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    logger = ctx.get('logger')
    logger.debug(f'POST /login with username "{form_data.username}" and password "{form_data.password}"')
    user = authenticate_user(ctx, form_data.username, form_data.password)

    if not user:
        logger.warning(f'Unauthorized login for username {form_data.username}: username not found.')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
