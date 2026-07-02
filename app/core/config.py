from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    SECRET_KEY: str = "changethisinsecretkeyinproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()