from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    HOST: str
    PORT: int
    TOKEN_EXP: int
    
    class Config:
        env_file = ".env"