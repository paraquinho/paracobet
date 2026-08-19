from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ParacoBet API"
    database_url: str = "postgresql+psycopg://paracobet:change-me@localhost:5432/paracobet"
    mock_data_enabled: bool = True
    use_database: bool = False
    environment: str = "development"
    cors_origins: str = "http://localhost:3000"
    sports_provider_api_key: str | None = None
    odds_provider_api_key: str | None = None
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")


settings = Settings()


def sqlalchemy_database_url() -> str:
    """Make plain libpq/Supabase URLs explicit for the psycopg SQLAlchemy driver."""
    url = settings.database_url
    if url.startswith("postgresql://"):
        url = "postgresql+psycopg://" + url.removeprefix("postgresql://")
    if ".supabase." in url and "sslmode=" not in url:
        url += "&sslmode=require" if "?" in url else "?sslmode=require"
    return url


def cors_origin_list() -> list[str]:
    return [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
