from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: SecretStr  # = 'postgres'
    postgres_password: SecretStr  # = 'postgrespw'
    db_host: str = "db"  # database service name in docker-compose.yml
    db_port: SecretStr  # = '5432'
    db_name: SecretStr  # = 'postgres'
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def database_url(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}".format(
            user=self.postgres_user.get_secret_value(),
            password=self.postgres_password.get_secret_value(),
            host=self.db_host,
            port=int(self.db_port.get_secret_value()),
            db_name=self.db_name.get_secret_value(),
        )


db_conf = Settings()
