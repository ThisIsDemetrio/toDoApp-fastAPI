from fastapi import APIRouter, Depends, HTTPException
from models.ToDoNote import ToDoNoteModel
from typing_extensions import Annotated
from config.get_context import get_context
from utils import generate_uuid

router = APIRouter(prefix="/note")

# Read an item
@router.get("/{id}", response_model=ToDoNoteModel)
async def get_by_id(id: str, ctx: Annotated[dict, Depends(get_context)]):
    logger = ctx.get('logger')
    try:
        collection = ctx.get('client').get_todo_collection()
        item = collection.find_one({"id": id})
        if item:
            return item
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.error(f'GET /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
##TODO: getAll

@router.post("/", response_model=dict)
async def create(item: ToDoNoteModel, ctx: Annotated[dict, Depends(get_context)]):
    logger = ctx.get('logger') 
    try:
        collection = ctx.get('client').get_todo_collection()

        item_id = generate_uuid()
        collection.insert_one({**item.model_dump(), "id": item_id})
        return {"status": "OK", "id": item_id}
    except Exception as e:
        logger.error(f'POST /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Update an item
@router.patch("/{id}", response_model=dict)
async def update(id: str, note_to_update: ToDoNoteModel, ctx: Annotated[dict, Depends(get_context)]):
    logger = ctx.get('logger')
    try:
        collection = ctx.get('client').get_todo_collection()

        result = collection.update_one({"id": id}, {"$set": note_to_update.model_dump()})
        if result.modified_count == 1:
            return {"status": "OK", "id": id}
        else:
            raise HTTPException(status_code=404, detail=f"Document with id {id} not found")
    except Exception as e:
        logger.error(f'PATCH /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

# Delete an item
@router.delete("/{id}", response_model=dict)
async def delete(id: str, ctx: Annotated[dict, Depends(get_context)]):
    logger = ctx.get('logger')
    try:
        collection = ctx.get('client').get_todo_collection()

        result = collection.delete_one({"id": id})
        if result.deleted_count == 1:
            return {"status": "OK"}
        else:
            raise HTTPException(status_code=404, detail=f"Document with id {id} not found.")
    except Exception as e:
        logger.error(f'DELETE /<id> returned error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
