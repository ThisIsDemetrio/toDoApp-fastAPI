from typing import List, Optional, Union
from fastapi import APIRouter,HTTPException
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
from models.ToDoNote import ToDoNoteModel
from app.get_context import Context

router = APIRouter(prefix="/note", tags=['Notes'])

@router.get("/", response_model=Union[List[ToDoNoteModel], dict])
async def get_all(ctx: Context, before: Optional[str] = None, after: Optional[str] = None):
    logger = ctx.get('logger')
    client = ctx.get('client')
        
    try:
        return await get_all_todos(client, before, after)
    except Exception as e:
        logger.error(f'GET / returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{id}", response_model=Union[ToDoNoteModel, dict])
async def get_by_id(ctx: Context, id: str):
    logger = ctx.get('logger')
    client = ctx.get('client')

    try:
        return await get_todo_by_id(client, id)
    except Exception as e:
        logger.error(f'GET /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.post("/", response_model=dict)
async def create(ctx: Context, item: ToDoNoteModel):
    logger = ctx.get('logger')
    client = ctx.get('client')

    try:
        return await create_todo(client, item)
    except Exception as e:
        logger.error(f'POST /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/{id}", response_model=dict)
async def update(ctx: Context, id: str, note_to_update: ToDoNoteModel):
    logger = ctx.get('logger')
    client = ctx.get('client')

    try:
        return await update_todo(client, id, note_to_update)
    except Exception as e:
        logger.error(f'POST /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/setToCompleted/{id}", response_model=dict)
async def set_to_completed(ctx: Context, id: str):
    logger = ctx.get('logger')
    client = ctx.get('client')

    try:
        return await set_todo_to_completed(client, id)
    except Exception as e:
        logger.error(f'PATCH /setToCompleted/<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.patch("/setToNotCompleted/{id}", response_model=dict)
async def set_to_not_completed(ctx: Context, id: str):
    logger = ctx.get('logger')
    client = ctx.get('client')

    try:
        return await set_todo_to_not_completed(client, id)
    except Exception as e:
        logger.error(f'PATCH /setToNotCompleted/<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.patch("/addRemainder/{id}", response_model=dict)
async def add_remainder(ctx: Context, id: str, new: str):
    logger = ctx.get('logger')
    client = ctx.get('client')

    try:
        return await add_remainder_to_todo(client, id, new)
    except Exception as e:
        logger.error(f'PATCH /addRemainder/<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.patch("/deleteRemainder/{id}", response_model=dict)
async def delete_remainder(ctx: Context, id: str, old: str):
    logger = ctx.get('logger')
    client = ctx.get('client')

    try:
        return await delete_remainder_to_todo(client, id, old)
    except Exception as e:
        logger.error(f'PATCH /deleteRemainder/<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.patch("/updateRemainder/{id}", response_model=dict)
async def update_remainder(ctx: Context, id: str, old: str, new: str):
    logger = ctx.get('logger')
    client = ctx.get('client')

    try:
        return await update_remainder_to_todo(client, id, old, new)
    except Exception as e:
        logger.error(f'PATCH /updateRemainder/<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{id}", response_model=dict)
async def delete(ctx: Context, id: str):
    logger = ctx.get('logger')
    client = ctx.get('client')

    try:
        return await delete_todo(client, id)
    except Exception as e:
        logger.error(f'DELETE /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
