from fastapi import FastAPI
from config.Client import Client
from config.Logger import Logger

from config.Settings import Settings

settings = Settings()
client = Client(settings)
logger = Logger(settings.log_level).get_logger()

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
