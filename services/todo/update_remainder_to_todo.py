from app import error_handling
from app.Client import Client
from utils.is_valid_iso_date import is_valid_iso_date


async def update_remainder_to_todo(client: Client, id: str, old_remainder: str, new_remainder: str):
    '''
    Change a remainder, replacing an existing one with a new one, to an existing note
    '''
    if not is_valid_iso_date(old_remainder):
        return error_handling.return_error(error_handling.A02, key="new_remainder")
    if not is_valid_iso_date(new_remainder):
        return error_handling.return_error(error_handling.A02, key="old_remainder")

    collection = client.get_todo_collection()

    pull_result = collection.update_one({"id":id}, {"$pull": {"remainders": old_remainder}})
    if pull_result.modified_count != 1:
        # TODO: Is this error because the remainder didn't exist, or the document has not been found?
        return error_handling.return_error(error_handling.C03)
    
    push_result = collection.update_one({"id":id}, {"$push": {"remainders": new_remainder}})
    if push_result.modified_count == 1:
        return {"status": "OK", "id": id}
    else:
        # TODO: What can happen to have an unhandled error?
        return error_handling.return_error(error_handling.U00)
