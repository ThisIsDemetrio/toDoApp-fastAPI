from app.Client import Client
from app.responses.IdNotFoundResponse import IdNotFoundResponse
from app.responses.SuccessResponse import SuccessResponse


async def delete_todo(
    client: Client, username: str, id: str
) -> SuccessResponse | IdNotFoundResponse:
    """
    Handle the deletion of a "todo" document
    """
    collection = client.get_todo_collection()

    result = collection.delete_one({"id": id, "user": username})
    if result.deleted_count == 1:
        return SuccessResponse(result=id)
    else:
        return IdNotFoundResponse(id=id)
