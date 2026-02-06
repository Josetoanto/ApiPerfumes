from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ApiPerfumes"

    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/perfumes_db"

    SECRET_KEY: str = "super-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
