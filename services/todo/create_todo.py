from datetime import datetime
from app.Client import Client
from models.Todo import ToDoModel
from utils.generate_uuid import generate_uuid


async def create_todo(client: Client, item: ToDoModel):
    """
    Create a new "todo" document.
    """
    collection = client.get_todo_collection()

    item_id = generate_uuid()
    current_iso_date = datetime.now().date().isoformat()
    collection.insert_one(
        {**item.model_dump(), "id": item_id, "creationDate": current_iso_date}
    )
    return {"status": "OK", "result": item_id}
