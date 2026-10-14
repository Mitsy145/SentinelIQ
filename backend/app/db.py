import logging
from functools import lru_cache

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings

log = logging.getLogger("sentineliq.db")


@lru_cache
def get_engine():
    return create_engine(get_settings().database_url, pool_pre_ping=True)


def check_database() -> bool:
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as exc:
        # Log only the error type: connection errors can contain host and user details.
        log.warning("database readiness check failed: %s", type(exc).__name__)
        return False
