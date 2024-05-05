from app.Client import Client
from app.responses.IdNotFoundResponse import IdNotFoundResponse
from app.responses.SuccessResponse import SuccessResponse


async def delete_remainder_to_todo(
    client: Client, username: str, id: str, remainder: str
) -> SuccessResponse | IdNotFoundResponse:
    """
    Remove an existing remainder to an existing "todo" document
    """

    collection = client.get_todo_collection()

    result = collection.update_one(
        {"id": id, "user": username}, {"$pull": {"remainders": remainder}}
    )
    if result.modified_count == 1:
        return SuccessResponse(result=id)
    else:
        # TODO: Is this error because the remainder didn't exist, or the document has not been found?
        return IdNotFoundResponse(id=id)
