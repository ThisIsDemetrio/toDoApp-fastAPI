from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.get_context import Context

from models.Signup import Signup
from models.Token import Token
from services.auth.create_user_and_generate_token import create_user_and_generate_token
from services.auth.login_and_generate_token import login_and_generate_token
from services.auth.utils import generate_token

# NOTE: I cannot use prefix because nested routes won't be found by oauth2_scheme. I guess I'll keep it that way
router = APIRouter(tags=["Authentication"])


@router.post("/signup")
async def signup(ctx: Context, form_data: Signup) -> Token:
    # TODO: form_data should be an actual form_data, perhaps
    logger = ctx.get("logger")

    logger.debug(
        f'POST /signup with username "{form_data.username}" and password "{form_data.password}"'
    )
    # TODO: We should check if username, password and email are valid and respect the validation rules, otherwise is 400

    try:
        # TODO: investigate if generating this token should also give me authentication
        result = create_user_and_generate_token(ctx, form_data)
        if result.get("status") == "KO":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=result.error_description
            )
        return result.get("token")
    except Exception as e:
        logger.error(f"POST /signup returned error: {e}")
        raise HTTPException(status_code=500, detail=e)


@router.post("/login")
async def login(
    ctx: Context, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    logger = ctx.get("logger")
    logger.debug(
        f'POST /login with username "{form_data.username}" and password "{form_data.password}"'
    )

    try:
        token = login_and_generate_token(ctx, form_data.username, form_data.password)
        if not token:
            logger.warning(
                f"Unauthorized login for username {form_data.username}: username not found."
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        logger.error(f"POST /login returned error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return generate_token(ctx, form_data.username)
