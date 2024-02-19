from fastapi import FastAPI
from app.Client import Client
from app.Settings import Settings
from app.get_context import Context, get_context
from api import Todo

ctx = get_context()

app = FastAPI(debug=ctx.get("settings").debug, title='ToDo App')
ctx.get("logger").debug(f'FastAPI Debug mode: {ctx.get("settings").debug}')

@app.get("/health", tags=['Health'])
def health(ctx: Context):
    logger = ctx.get('logger')
    
    logger.debug('Health check requested.')
    return {"status": "OK"}

@app.get("/db-health", tags=['Health'])
async def db_health(ctx: Context):
    logger: Settings = ctx.get('logger')
    client: Client = ctx.get('client')

    logger.debug('DB Health check requested')
    documents_in_config_coll = client.get_config_collection().estimated_document_count({})

    return {"status": "OK", "existingConfigs": documents_in_config_coll}

app.include_router(Todo.router)
