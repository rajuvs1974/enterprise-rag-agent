from erap.config.settings import get_settings


def test_default_settings() -> None:
    settings = get_settings()

    assert settings.app_name == "Enterprise RAG Agent"
    assert settings.environment == "development"
    assert settings.debug is False

def test_database_configuration() -> None:
    settings = get_settings()

    assert settings.database_url.startswith("postgresql+asyncpg://")