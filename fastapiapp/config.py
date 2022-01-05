from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host_languages: str
    db_port_languages: str
    db_pass_languages: str
    db_name_languages: str
    db_user_languages: str
    secret_key_languages: str
    algorithm_languages: str
    ACCESS_TOKEN_EXPIRE_MINUTES_languages: int
    DB_HOST: str
    DB_PORT: str
    DB_PASS: str
    DB_NAME: str
    DB_USER: str
    secret_key: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    postgres_redis: str

    class Config:
        env_file = ".env"


settings = Settings()