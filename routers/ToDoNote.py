from datetime import datetime
from typing import List, Optional, Union
from fastapi import APIRouter,HTTPException
from application.utils import is_valid_iso_date
from config import error_handling
from models.ToDoNote import ToDoNoteModel
from config.get_context import Context
from utils import generate_uuid

router = APIRouter(prefix="/note", tags=['Notes'])

@router.get("/", response_model=Union[List[ToDoNoteModel], dict])
async def get_all(ctx: Context, before: Optional[str] = None, after: Optional[str] = None):
    logger = ctx.get('logger')
    query = {}
    
    if (before is not None):
        if not is_valid_iso_date(before):
            return error_handling.return_error(error_handling.A02, key="before")
        query["$lte"] = before
    
    if (after is not None):
        if not is_valid_iso_date(after):
            return error_handling.return_error(error_handling.A02, key="after")
        query["$gte"] = after
        
    try:
        collection = ctx.get('client').get_todo_collection()
        return collection.find({ "creationDate": query } if len(query.keys()) > 0 else {}).limit(50)
    except Exception as e:
        logger.error(f'GET / returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{id}", response_model=Union[ToDoNoteModel, dict])
async def get_by_id(ctx: Context, id: str):
    '''
    Returns the note with a specific "id" passed in query string.
    Returns a 404 exception if the document is not found.
    '''
    logger = ctx.get('logger')
    try:
        collection = ctx.get('client').get_todo_collection()
        item = collection.find_one({"id": id})
        if item:
            return item
        else:
            return error_handling.return_error(error_handling.A01, id=id)
    except Exception as e:
        logger.error(f'GET /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.post("/", response_model=dict)
async def create(ctx: Context, item: ToDoNoteModel):
    '''
    Create a new note.
    '''
    logger = ctx.get('logger') 
    try:
        collection = ctx.get('client').get_todo_collection()

        item_id = generate_uuid()
        current_iso_date = datetime.now().date().isoformat()
        collection.insert_one({**item.model_dump(), "id": item_id, "creationDate": current_iso_date })
        return {"status": "OK", "id": item_id}
    except Exception as e:
        logger.error(f'POST /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/{id}", response_model=dict)
async def update(ctx: Context, id: str, note_to_update: ToDoNoteModel):
    '''
    Update the note with the "id" included in the request.
    Returns a 404 Exception if the document does not exist.
    '''
    logger = ctx.get('logger')
    try:
        collection = ctx.get('client').get_todo_collection()

        result = collection.update_one({"id": id}, {"$set": note_to_update.model_dump()})
        if result.modified_count == 1:
            return {"status": "OK", "id": id}
        else:
            return error_handling.return_error(error_handling.A01, id=id)
    except Exception as e:
        logger.error(f'PATCH /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/setToCompleted/{id}", response_model=dict)
async def setToCompleted(ctx: Context, id: str):
    '''
    Set the "completed" flag on a note to "True"
    '''
    logger = ctx.get('logger')
    try:
        collection = ctx.get('client').get_todo_collection()

        result = collection.update_one({"id":id, "completed": False}, {"$set": {"completed": True}})   
        if result.modified_count == 1:
            return {"status": "OK", "id": id}
        else:
            # TODO: Is this error because the note was already completed, or it has not been found?
            return error_handling.return_error(error_handling.C01)
    except Exception as e:
        logger.error(f'PATCH /setToCompleted/<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/setToNotCompleted/{id}", response_model=dict)
async def setToNotCompleted(ctx: Context, id: str):
    '''
    Set the "completed" flag on a note to "False"
    '''
    logger = ctx.get('logger')
    try:
        collection = ctx.get('client').get_todo_collection()

        result = collection.update_one({"id":id, "completed": True}, {"$set": {"completed": False}})   
        if result.modified_count == 1:
            return {"status": "OK", "id": id}
        else:
            # TODO: Is this error because the note was already not completed, or it has not been found?
            return error_handling.return_error(error_handling.C02)
    except Exception as e:
        logger.error(f'PATCH /setToNotCompleted/<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.delete("/{id}", response_model=dict)
async def delete(ctx: Context, id: str):
    '''
    Handle the deletion of a note
    '''
    logger = ctx.get('logger')
    try:
        collection = ctx.get('client').get_todo_collection()

        result = collection.delete_one({"id": id})
        if result.deleted_count == 1:
            return {"status": "OK"}
        else:
            return error_handling.return_error(error_handling.A01, id=id)
    except Exception as e:
        logger.error(f'DELETE /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
