from fastapi import FastAPI
from config.Client import Client
from config.Logger import Logger

from config.Settings import Settings

ctx = {}
ctx['settings'] = Settings()
ctx['client'] = Client(ctx.get('settings'))
ctx['logger'] = Logger(ctx.get('settings').log_level).get_logger()

app = FastAPI()
# TODO: Debug mode via env var

@app.get("/health")
def health():
    logger = ctx.get('logger')
    
    logger.debug('Health check requested.')
    return {"status": "OK"}
