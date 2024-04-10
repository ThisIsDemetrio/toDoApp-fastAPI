from app import error_handling
from app.Client import Client
from app.ErrorCode import ErrorCode
from utils.is_valid_iso_date import is_valid_iso_date


async def delete_remainder_to_todo(client: Client, id: str, remainder: str):
    '''
    Remove an existing remainder to an existing "todo" document
    '''
    if not is_valid_iso_date(remainder):
        return error_handling.return_error(ErrorCode.A02, key="payload")

    collection = client.get_todo_collection()

    result = collection.update_one({"id":id}, {"$pull": {"remainders": remainder}})   
    if result.modified_count == 1:
        return {"status": "OK", "id": id}
    else:
        # TODO: Is this error because the remainder didn't exist, or the document has not been found?
        return error_handling.return_error(ErrorCode.C03)
