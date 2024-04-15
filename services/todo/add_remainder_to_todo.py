from app.error_handling import return_error, ErrorModel
from app.Client import Client, ReturnModel
from app.ErrorCode import ErrorCode
from utils.is_valid_iso_date import is_valid_iso_date


async def add_remainder_to_todo(
    client: Client, id: str, remainder: str
) -> ReturnModel | ErrorModel:
    """
    Add a new remainder to an existing "todo" document
    """
    if not is_valid_iso_date(remainder):
        return return_error(ErrorCode.A02, key="payload")

    collection = client.get_todo_collection()

    result = collection.update_one({"id": id}, {"$push": {"remainders": remainder}})
    if result.modified_count == 1:
        return {"status": "OK", "result": id}
    else:
        # NOTE: I am assuming the only error can occur is because the document has not been found
        return return_error.return_error(ErrorCode.A01)
