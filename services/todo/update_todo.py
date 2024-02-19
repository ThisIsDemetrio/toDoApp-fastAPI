from app import error_handling
from app.Client import Client
from models.ToDoNote import ToDoNoteModel

async def update_todo(client: Client, id: str, note_to_update: ToDoNoteModel):
    '''
    Update the note with the "id" included in the request.
    Returns a 404 Exception if the document does not exist.
    '''
    collection = client.get_todo_collection()

    result = collection.update_one({"id": id}, {"$set": note_to_update.model_dump()})
    if result.modified_count == 1:
        return {"status": "OK", "id": id}
    else:
        return error_handling.return_error(error_handling.A01, id=id)
