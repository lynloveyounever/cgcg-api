from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEADLINE_WEBSERVICE_URL: str = "http://localhost:8082"
    
    # Add other application-wide settings here

    class Config:
        # In a real application, you might load this from a .env file
        env_file = ".env"

# Create a single, importable instance of the settings
settings = Settings()