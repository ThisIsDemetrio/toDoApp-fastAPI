from app.Client import Client
from app.responses.IdNotFoundResponse import IdNotFoundResponse
from app.responses.SuccessResponse import SuccessResponse


async def get_todo_by_id(
    client: Client, username: str, id: str
) -> SuccessResponse | IdNotFoundResponse:
    """
    Returns the "todo" document with a specific "id" passed in query string.
    Returns a 404 exception if the document is not found.
    """
    collection = client.get_todo_collection()
    item = collection.find_one({"id": id, "user": username}, {"_id": 0})
    if item:
        return SuccessResponse(result=item)
    else:
        return IdNotFoundResponse(id=id)
