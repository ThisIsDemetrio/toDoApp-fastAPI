from datetime import datetime
from app.Client import Client
from models.ToDoNote import ToDoNoteModel
from utils.generate_uuid import generate_uuid

async def create_todo(client: Client, item: ToDoNoteModel):
    '''
    Create a new note.
    '''
    collection = client.get_todo_collection()

    item_id = generate_uuid()
    current_iso_date = datetime.now().date().isoformat()
    collection.insert_one({**item.model_dump(), "id": item_id, "creationDate": current_iso_date })
    return {"status": "OK", "id": item_id}
