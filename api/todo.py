from typing import Annotated, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status

from app.responses.InvalidDateBadRequest import InvalidDateBadRequest
from app.responses.LimitNotValidBadRequest import LimitNotValidBadRequest
from app.get_context import Context
from models.Todo import ToDoModel
from models.User import User
from services.auth.utils import get_current_active_user
from services.todo.add_remainder_to_todo import add_remainder_to_todo
from services.todo.create_todo import create_todo
from services.todo.delete_remainder_to_todo import delete_remainder_to_todo
from services.todo.delete_todo import delete_todo
from services.todo.get_all_todos import get_all_todos
from services.todo.get_todo_by_id import get_todo_by_id
from services.todo.set_todo_to_completed import set_todo_to_completed
from services.todo.set_todo_to_not_completed import set_todo_to_not_completed
from services.todo.update_remainder_to_todo import update_remainder_to_todo
from services.todo.update_todo import update_todo
from utils.is_valid_iso_date import is_valid_iso_date

router = APIRouter(prefix="/todo", tags=["To Do notes"])


@router.get(
    "/",
    response_model=Union[List[ToDoModel], dict],
    dependencies=[Depends(get_current_active_user)],
)
async def get_all(
    current_user: Annotated[User, Depends(get_current_active_user)],
    ctx: Context,
    before: Optional[str] = None,
    after: Optional[str] = None,
    completed: Optional[bool] = None,
    limit: Optional[str] = None,
):
    logger = ctx.get("logger")
    client = ctx.get("client")
    username = current_user.get("username")

    if before is not None and not is_valid_iso_date(before):
        return InvalidDateBadRequest(key="before", value=before)

    if after is not None and not is_valid_iso_date(after):
        return InvalidDateBadRequest(key="after", value=after)

    # Check if limit is of type int and it is positive
    if limit is not None:
        try:
            limit = int(limit)
        except ValueError:
            return LimitNotValidBadRequest()

        if limit <= 0:
            return LimitNotValidBadRequest()

    try:
        return await get_all_todos(
            client, username, before, after, completed, limit
        )
    except Exception as e:
        logger.error(f"GET / returned error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/{id}",
    response_model=Union[ToDoModel, dict],
    dependencies=[Depends(get_current_active_user)],
)
async def get_by_id(
    current_user: Annotated[User, Depends(get_current_active_user)],
    ctx: Context,
    id: str,
):
    logger = ctx.get("logger")
    client = ctx.get("client")
    username = current_user.get("username")

    try:
        return await get_todo_by_id(client, username, id)
    except Exception as e:
        logger.error(f"GET /<id> returned error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post(
    "/", response_model=dict, dependencies=[Depends(get_current_active_user)]
)
async def create(
    current_user: Annotated[User, Depends(get_current_active_user)],
    ctx: Context,
    item: ToDoModel,
):
    logger = ctx.get("logger")
    client = ctx.get("client")
    username = current_user.get("username")

    try:
        return await create_todo(client, username, item)
    except Exception as e:
        logger.error(f"POST /<id> returned error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put(
    "/{id}",
    response_model=dict,
    dependencies=[Depends(get_current_active_user)],
)
async def update(
    current_user: Annotated[User, Depends(get_current_active_user)],
    ctx: Context,
    id: str,
    todo_to_update: ToDoModel,
):
    logger = ctx.get("logger")
    client = ctx.get("client")
    username = current_user.get("username")

    if todo_to_update.user != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{username} trying to modify todo document fo another user",
        )

    try:
        return await update_todo(client, id, todo_to_update)
    except Exception as e:
        logger.error(f"PUT /<id> returned error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch(
    "/setToCompleted/{id}",
    response_model=dict,
    dependencies=[Depends(get_current_active_user)],
)
async def set_to_completed(
    current_user: Annotated[User, Depends(get_current_active_user)],
    ctx: Context,
    id: str,
):
    logger = ctx.get("logger")
    client = ctx.get("client")
    username = current_user.get("username")

    try:
        return await set_todo_to_completed(client, username, id)
    except Exception as e:
        logger.error(f"PATCH /setToCompleted/<id> returned error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch(
    "/setToNotCompleted/{id}",
    response_model=dict,
    dependencies=[Depends(get_current_active_user)],
)
async def set_to_not_completed(
    current_user: Annotated[User, Depends(get_current_active_user)],
    ctx: Context,
    id: str,
):
    logger = ctx.get("logger")
    client = ctx.get("client")
    username = current_user.get("username")

    try:
        return await set_todo_to_not_completed(client, username, id)
    except Exception as e:
        logger.error(f"PATCH /setToNotCompleted/<id> returned error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch(
    "/addRemainder/{id}",
    response_model=dict,
    dependencies=[Depends(get_current_active_user)],
)
async def add_remainder(
    current_user: Annotated[User, Depends(get_current_active_user)],
    ctx: Context,
    id: str,
    new: str,
):
    logger = ctx.get("logger")
    client = ctx.get("client")
    username = current_user.get("username")

    if not is_valid_iso_date(new):
        return InvalidDateBadRequest(key="new", value=new)

    try:
        return await add_remainder_to_todo(client, username, id, new)
    except Exception as e:
        logger.error(f"PATCH /addRemainder/<id> returned error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch(
    "/deleteRemainder/{id}",
    response_model=dict,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_remainder(
    current_user: Annotated[User, Depends(get_current_active_user)],
    ctx: Context,
    id: str,
    old: str,
):
    logger = ctx.get("logger")
    client = ctx.get("client")
    username = current_user.get("username")

    if not is_valid_iso_date(old):
        return InvalidDateBadRequest(key="old", value=old)

    try:
        return await delete_remainder_to_todo(client, username, id, old)
    except Exception as e:
        logger.error(f"PATCH /deleteRemainder/<id> returned error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch(
    "/updateRemainder/{id}",
    response_model=dict,
    dependencies=[Depends(get_current_active_user)],
)
async def update_remainder(
    current_user: Annotated[User, Depends(get_current_active_user)],
    ctx: Context,
    id: str,
    old: str,
    new: str,
):
    logger = ctx.get("logger")
    client = ctx.get("client")
    username = current_user.get("username")

    if not is_valid_iso_date(old):
        return InvalidDateBadRequest(key="old", value=old)

    if not is_valid_iso_date(new):
        return InvalidDateBadRequest(key="new", value=new)

    try:
        return await update_remainder_to_todo(client, username, id, old, new)
    except Exception as e:
        logger.error(f"PATCH /updateRemainder/<id> returned error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete(
    "/{id}",
    response_model=dict,
    dependencies=[Depends(get_current_active_user)],
)
async def delete(
    current_user: Annotated[User, Depends(get_current_active_user)],
    ctx: Context,
    id: str,
):
    logger = ctx.get("logger")
    client = ctx.get("client")
    username = current_user.get("username")

    try:
        return await delete_todo(client, username, id)
    except Exception as e:
        logger.error(f"DELETE /<id> returned error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
