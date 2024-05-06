from app.Client import Client
from app.responses.NotCompletedYetResponse import NotCompletedYetResponse
from app.responses.SuccessResponse import SuccessResponse


async def set_todo_to_not_completed(
    client: Client, username: str, id: str
) -> SuccessResponse | NotCompletedYetResponse:
    """
    Set the "completed" flag on a "todo" document to "False"
    """
    collection = client.get_todo_collection()

    result = collection.update_one(
        {"id": id, "user": username, "completed": True},
        {"$set": {"completed": False}},
    )
    if result.modified_count == 1:
        return SuccessResponse(result=id)
    else:
        # TODO: Is this error because the todo was already completed, or it has not been found, or the user is wrong?
        return NotCompletedYetResponse(id=id)
