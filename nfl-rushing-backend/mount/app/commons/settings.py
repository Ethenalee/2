from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "nfl-rushing-service"
    APP_ENV: str = "local"
    APP_COMPONENT: str = "server"
    SERVER_PORT: int = 5000
    DB_MAX_POOL_SIZE: int = 2
    DB_MIN_POOL_SIZE: int = 1
    DB_NAME: str = "rushing_dev"
    DB_SSL: str = "prefer"
    CONNECTION_RETRIES: int = 5
    READ_DB_HOST: str = "postgres"
    READ_DB_PASS: str = "password"
    READ_DB_PORT: int = 5432
    READ_DB_USER: str = "postgres"
    WRITE_DB_HOST: str = "postgres"
    WRITE_DB_PASS: str = "password"
    WRITE_DB_PORT: int = 5432
    WRITE_DB_USER: str = "postgres"


settings = Settings(_env_file=".env")
