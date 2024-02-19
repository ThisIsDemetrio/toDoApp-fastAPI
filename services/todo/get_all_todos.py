from typing import Optional

from app import Client, error_handling
from utils.is_valid_iso_date import is_valid_iso_date

async def get_all_todos(client: Client, before: Optional[str] = None, after: Optional[str] = None):
    '''
    Search all the items in the database.

    The search could be filtered with a before and an after, related to the date of creation.
    '''
    query = {}
    
    if (before is not None):
        if not is_valid_iso_date(before):
            return error_handling.return_error(error_handling.A02, key="before")
        query["$lte"] = before
    
    if (after is not None):
        if not is_valid_iso_date(after):
            return error_handling.return_error(error_handling.A02, key="after")
        query["$gte"] = after
        
    collection = client.get_todo_collection()
    # TODO: We're returning 1000 elements, but we should handle pagination or something
    return collection.find({ "creationDate": query } if len(query.keys()) > 0 else {}).limit(1000)
