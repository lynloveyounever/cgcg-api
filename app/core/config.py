from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import List

# Defines the configuration for a single loadable module
class ModuleConfig(BaseModel):
    name: str         # A unique name for the module
    path: str         # The Python import path (e.g., "app.modules.deadline")
    enabled: bool = True  # A flag to enable or disable loading

class Settings(BaseSettings):
    DEADLINE_WEBSERVICE_URL: str = "http://localhost:8082"
    
    # A list of all modules the application should attempt to load.
    # You can disable modules here or even load them from different source paths.
    MODULES: List[ModuleConfig] = [
        ModuleConfig(name="Deadline", path="app.modules.deadline", enabled=True),
        ModuleConfig(name="Media Shuttle", path="app.modules.media_shuttle", enabled=True),
        ModuleConfig(name="user", path="app.modules.user", enabled=True),
    ]

    class Config:
        # In a real application, you might load this from a .env file
        env_file = ".env"

# Create a single, importable instance of the settings
settings = Settings()
