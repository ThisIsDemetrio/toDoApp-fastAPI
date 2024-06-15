from typing import Optional

from pymongo.collection import Collection

from app import Client
from app.responses.SuccessResponse import SuccessResponse


DEFAULT_LIMIT = 200


async def get_all_todos(
    client: Client,
    username: str,
    before: Optional[str] = None,
    after: Optional[str] = None,
    completed: Optional[bool] = None,
    limit: Optional[int] = None,
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

    query = {"user": username}

    if completed is not None:
        query.update({"completed": completed})
    if len(timespan_query.keys()) > 0:
        query.update({"creationDate": timespan_query})

    collection: Collection = client.get_todo_collection()
    documents = collection.find(query, {"_id": 0}).limit(
        limit or DEFAULT_LIMIT
    )

    return SuccessResponse(result=list(documents))
