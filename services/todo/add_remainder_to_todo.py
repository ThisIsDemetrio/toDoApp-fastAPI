from app import error_handling
from app.Client import Client
from utils.is_valid_iso_date import is_valid_iso_date


async def add_remainder_to_todo(client: Client, id: str, remainder: str):
    '''
    Add a new remainder to an existing note
    '''
    if not is_valid_iso_date(remainder):
        return error_handling.return_error(error_handling.A02, key="payload")

    collection = client.get_todo_collection()

    result = collection.update_one({"id":id}, {"$push": {"remainders": remainder}})   
    if result.modified_count == 1:
        return {"status": "OK", "id": id}
    else:
        # NOTE: I am assuming the only error can occur is because the document has not been found
        return error_handling.return_error(error_handling.A01)
