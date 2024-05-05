from typing import Optional

from pymongo.collection import Collection

from app import Client
from app.responses.SuccessResponse import SuccessResponse


async def get_all_todos(
    client: Client,
    username: str,
    before: Optional[str] = None,
    after: Optional[str] = None,
) -> SuccessResponse:
    """
    Search all the items in the database.

    The search could be filtered with a before and an after, related to the date of creation.
    """
    timespan_query = {}

    if before is not None:
        timespan_query["$lte"] = before

    if after is not None:
        timespan_query["$gte"] = after

    collection: Collection = client.get_todo_collection()

    query = {"user": username}
    if len(timespan_query.keys()) > 0:
        query.update({"creationDate": timespan_query})

    # TODO: We're returning 1000 elements, but we should handle pagination or something
    documents = collection.find(query, {"_id": 0}).limit(1000)
    return SuccessResponse(result=list(documents))
