from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.get_context import Context
from app.auth import oauth2_scheme

from models.User import User
from models.Token import Token
from services.auth.utils import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user

# TODO: Move logic to services
# TODO: Add route to add users
# TODO: Attach all of this to /todo/ routes

# NOTE: I cannot use prefix because nested routes won't be found by oauth2_scheme. I guess I'll keep it that way 
router = APIRouter(tags=['Authentication'])

@router.post("/token")
async def login(ctx: Context, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    logger = ctx.get('logger')
    logger.debug(f'POST /token with username "{form_data.username}" and password "{form_data.password}"')
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

# TODO: This must disappear
@router.get("/auth/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

# TODO: This must disappear
@router.get("/auth/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

# TODO: This must disappear
@router.get("/auth/items")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
