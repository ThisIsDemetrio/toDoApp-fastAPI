from fastapi import FastAPI
from pymongo import MongoClient
from config.Client import Client

from config.Settings import Settings

app = FastAPI()

ctx = {}
ctx['settings'] = Settings()
ctx['client'] = Client(ctx.get('settings'))
# TODO: Add logger to the ctx

@app.get("/health")
def health():
    return {"status": "OK"}
