from app.Client import Client
from app.responses.IdNotFoundResponse import IdNotFoundResponse
from app.responses.NotExecutedResponse import NotExecutedResponse
from app.responses.SuccessResponse import SuccessResponse


async def update_remainder_to_todo(
    client: Client,
    username: str,
    id: str,
    old_remainder: str,
    new_remainder: str,
) -> SuccessResponse | IdNotFoundResponse | NotExecutedResponse:
    """
    Change a remainder, replacing an existing one with a new one, to an existing "todo" document
    """

    collection = client.get_todo_collection()

    pull_result = collection.update_one(
        {"id": id, "user": username}, {"$pull": {"remainders": old_remainder}}
    )
    if pull_result.modified_count != 1:
        # TODO: Is this error because the remainder didn't exist, or the document has not been found?
        return IdNotFoundResponse(id=id)

    push_result = collection.update_one(
        {"id": id, "user": username}, {"$push": {"remainders": new_remainder}}
    )

    if push_result.modified_count == 1:
        return SuccessResponse(result=id)
    else:
        # TODO: What can happen to have an unhandled error?
        return NotExecutedResponse()
