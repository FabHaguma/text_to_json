from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    gemini_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def api_key(self) -> Optional[str]:
        return self.gemini_api_key or self.google_api_key

settings = Settings()
