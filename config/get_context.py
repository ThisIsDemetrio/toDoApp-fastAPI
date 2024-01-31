from config.Settings import Settings
from config.Logger import Logger
from config.Client import Client 

# TODO: Evaluate if to create different context for different router modules (to return the collection instead than the whole client)
# TODO: Create model or class
# TODO: can we lruCache this?

def get_context():
    """Create a dict with logger, client, etc.. to be injected in routes"""
    settings: Settings = Settings()
    logger: Logger = Logger(settings.log_level).get_logger()
    client: Client = Client(settings.mongo_url, settings.database_name)

    return {
        "settings": settings,
        "client": client,
        "logger": logger
    }
