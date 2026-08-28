import logging
import sys

from erap.config.settings import get_settings


def configure_logging() -> None:
    """Configure application-wide structured logging."""
    settings = get_settings()

    logging.basicConfig(
        level=logging.INFO if not settings.debug else logging.DEBUG,
        format=(
            "%(asctime)s | %(levelname)s | "
            f"{settings.app_name} | %(name)s | %(message)s"
        ),
        stream=sys.stdout,
        force=True,
    )