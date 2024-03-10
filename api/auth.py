from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.get_context import Context
from app.auth import oauth2_scheme

from models.User import User
from models.Token import Token
from services.auth.utils import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user

# NOTE: I cannot use prefix because nested routes won't be found by oauth2_scheme. I guess I'll keep it that way 
router = APIRouter(tags=['Authentication'])

@router.post("/token")
async def login_for_access_token(ctx: Context, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    pwd_context = ctx.get('pwd_context')

    # TODO: Connect to database
    # client = ctx.get('client')
    user = authenticate_user(pwd_context, form_data.username, form_data.password)

    if not user:
        # TODO: Attach logger
        # TODO: Use custom error, perhaps?
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

@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
