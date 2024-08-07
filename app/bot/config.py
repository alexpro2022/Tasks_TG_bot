from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    emoji: bool = True
    bot_token: SecretStr = "1111111111:AAAAAAAAAAAAAAAAA-BBB_CCCCCCCCCCCCC"
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


conf = Settings()
