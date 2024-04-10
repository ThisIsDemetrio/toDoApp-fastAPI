from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils import DATABASE_NAME

class Settings(BaseSettings):
    debug: bool = True
    mongo_url: str
    database_name: str = DATABASE_NAME
    log_level: str = ''
    hash_key: str = ''
    
    model_config = SettingsConfigDict(env_file=".env")
