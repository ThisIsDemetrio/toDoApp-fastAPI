from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from config import error_handling
from models.ToDoNote import ToDoNoteModel
from typing_extensions import Annotated
from config.get_context import get_context
from utils import generate_uuid

router = APIRouter(prefix="/note")

@router.get("/{id}", response_model=Union[ToDoNoteModel, dict])
async def get_by_id(id: str, ctx: Annotated[dict, Depends(get_context)]):
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
    
##TODO: getAll

@router.post("/", response_model=dict)
async def create(item: ToDoNoteModel, ctx: Annotated[dict, Depends(get_context)]):
    '''
    Create a new note.
    '''
    logger = ctx.get('logger') 
    try:
        collection = ctx.get('client').get_todo_collection()

        item_id = generate_uuid()
        collection.insert_one({**item.model_dump(), "id": item_id})
        return {"status": "OK", "id": item_id}
    except Exception as e:
        logger.error(f'POST /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/{id}", response_model=dict)
async def update(id: str, note_to_update: ToDoNoteModel, ctx: Annotated[dict, Depends(get_context)]):
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
async def setToCompleted(id: str, ctx: Annotated[dict, Depends(get_context)]):
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
async def setToNotCompleted(id: str, ctx: Annotated[dict, Depends(get_context)]):
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
async def delete(id: str, ctx: Annotated[dict, Depends(get_context)]):
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
