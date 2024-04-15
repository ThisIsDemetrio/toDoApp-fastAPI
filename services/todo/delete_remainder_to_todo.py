from app.Client import Client, ReturnModel
from app.error_handling import ErrorModel, return_error
from app.ErrorCode import ErrorCode
from utils.is_valid_iso_date import is_valid_iso_date


async def delete_remainder_to_todo(
    client: Client, username: str, id: str, remainder: str
) -> ReturnModel | ErrorModel:
    """
    Remove an existing remainder to an existing "todo" document
    """
    if not is_valid_iso_date(remainder):
        return return_error(ErrorCode.A02, key="payload")

    collection = client.get_todo_collection()

    result = collection.update_one(
        {"id": id, "user": username}, {"$pull": {"remainders": remainder}}
    )
    if result.modified_count == 1:
        return {"status": "OK", "result": id}
    else:
        # TODO: Is this error because the remainder didn't exist, or the document has not been found?
        return return_error(ErrorCode.A01)
