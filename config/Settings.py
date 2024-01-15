from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    debug: bool = True
    mongo_url: str
    log_level: str = ''
    
    model_config = SettingsConfigDict(env_file=".env")