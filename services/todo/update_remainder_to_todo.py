from app.Client import Client, ReturnModel
from app.error_handling import ErrorModel, return_error
from app.ErrorCode import ErrorCode


async def update_remainder_to_todo(
    client: Client,
    username: str,
    id: str,
    old_remainder: str,
    new_remainder: str,
) -> ReturnModel | ErrorModel:
    """
    Change a remainder, replacing an existing one with a new one, to an existing "todo" document
    """

    collection = client.get_todo_collection()

    pull_result = collection.update_one(
        {"id": id, "user": username}, {"$pull": {"remainders": old_remainder}}
    )
    if pull_result.modified_count != 1:
        # TODO: Is this error because the remainder didn't exist, or the document has not been found?
        return return_error(ErrorCode.A01)

    push_result = collection.update_one(
        {"id": id, "user": username}, {"$push": {"remainders": new_remainder}}
    )
    if push_result.modified_count == 1:
        return {"status": "OK", "result": id}
    else:
        # TODO: What can happen to have an unhandled error?
        return return_error(ErrorCode.U00)
