from app.Client import Client, ReturnModel
from app.error_handling import ErrorModel, return_error
from app.ErrorCode import ErrorCode


async def add_remainder_to_todo(
    client: Client, username: str, id: str, remainder: str
) -> ReturnModel | ErrorModel:
    """
    Add a new remainder to an existing "todo" document
    """

    collection = client.get_todo_collection()

    result = collection.update_one(
        {"id": id, "user": username}, {"$push": {"remainders": remainder}}
    )
    if result.modified_count == 1:
        return {"status": "OK", "result": id}
    else:
        # NOTE: I am assuming the only error can occur is because the document has not been found
        return return_error(ErrorCode.A01)
