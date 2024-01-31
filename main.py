from fastapi import Depends, FastAPI
from typing_extensions import Annotated
from config.Client import Client
from config.Settings import Settings
from config.get_context import get_context
from routers import ToDoNote

ctx = get_context()

app = FastAPI(debug=ctx.get("settings").debug, title='ToDo App')
ctx.get("logger").debug(f'FastAPI Debug mode: {ctx.get("settings").debug}')

@app.get("/health")
def health(ctx: Annotated[dict, Depends(get_context)]):
    logger = ctx.get('logger')
    
    logger.debug('Health check requested.')
    return {"status": "OK"}

@app.get("/db-health")
async def db_health(ctx: Annotated[dict, Depends(get_context)]):
    logger: Settings = ctx.get('logger')
    client: Client = ctx.get('client')

    logger.debug('DB Health check requested')
    documents_in_config_coll = client.get_config_collection().estimated_document_count({})

    return {"status": "OK", "existingConfigs": documents_in_config_coll}

app.include_router(ToDoNote.router)
