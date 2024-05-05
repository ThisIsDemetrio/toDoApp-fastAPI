from app.Client import Client
from app.responses.IdNotFoundResponse import IdNotFoundResponse
from app.responses.SuccessResponse import SuccessResponse


async def add_remainder_to_todo(
    client: Client, username: str, id: str, remainder: str
) -> SuccessResponse | IdNotFoundResponse:
    """
    Add a new remainder to an existing "todo" document
    """

    collection = client.get_todo_collection()

    result = collection.update_one(
        {"id": id, "user": username}, {"$push": {"remainders": remainder}}
    )
    if result.modified_count == 1:
        return SuccessResponse(result=id)
    else:
        # NOTE: I am assuming the only error can occur is because the document has not been found
        return IdNotFoundResponse(id=id)
