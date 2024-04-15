from typing import Optional
from pymongo.collection import Collection

from app import Client
from app.Client import ReturnModel
from app.ErrorCode import ErrorCode
from app.error_handling import ErrorModel, return_error
from utils.is_valid_iso_date import is_valid_iso_date


async def get_all_todos(
    client: Client, before: Optional[str] = None, after: Optional[str] = None
) -> ReturnModel | ErrorModel:
    """
    Search all the items in the database.

    The search could be filtered with a before and an after, related to the date of creation.
    """
    query = {}

    if before is not None:
        if not is_valid_iso_date(before):
            return return_error(ErrorCode.A02, key="before")
        query["$lte"] = before

    if after is not None:
        if not is_valid_iso_date(after):
            return return_error(ErrorCode.A02, key="after")
        query["$gte"] = after

    collection: Collection = client.get_todo_collection()

    # TODO: We're returning 1000 elements, but we should handle pagination or something
    documents = collection.find(
        {"creationDate": query} if len(query.keys()) > 0 else {}, {"_id": 0}
    ).limit(1000)
    return {"status": "OK", "result": documents}
