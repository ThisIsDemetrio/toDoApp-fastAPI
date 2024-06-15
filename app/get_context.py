from typing import Annotated
from fastapi import Depends
from app.Settings import Settings
from app.Logger import Logger
from passlib.context import CryptContext
from app.Client import Client

# TODO: Evaluate if to create different context for different router modules (to return the collection instead than the whole client)
# TODO: Create model or class
# TODO: can we lruCache this?


def get_context():
    """Create a dict with logger, client, etc.. to be injected in routes"""
    settings: Settings = Settings()
    logger: Logger = Logger(settings.log_level).get_logger()
    client: Client = Client(settings.mongo_url, settings.database_name)
    pwd_context: CryptContext = CryptContext(
        schemes=["bcrypt"], deprecated="auto"
    )

    return {
        "settings": settings,
        "client": client,
        "logger": logger,
        "pwd_context": pwd_context,
    }


Context = Annotated[dict, Depends(get_context)]
