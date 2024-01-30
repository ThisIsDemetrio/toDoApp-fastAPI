from fastapi import FastAPI
from config.Client import Client
from config.Logger import Logger

from config.Settings import Settings

settings: Settings = Settings()
client: Client = Client(settings)
logger: Logger = Logger(settings.log_level).get_logger()

ctx = {}
ctx['settings'] = settings
ctx['client'] = client
ctx['logger'] = logger

app = FastAPI(debug=settings.debug, title='ToDo App')

logger.debug(f'FastAPI Debug mode: {settings.debug}')

@app.get("/health")
def health():
    logger = ctx.get('logger')
    
    logger.debug('Health check requested.')
    return {"status": "OK"}

@app.get("/db-health")
async def db_health():
    logger: Settings = ctx.get('logger')
    client: Client = ctx.get('client')

    logger.debug('DB Health check requested')
    documents_in_config_coll = client.get_config_collection().estimated_document_count({})

    return {"status": "OK", "existingConfigs": documents_in_config_coll}
