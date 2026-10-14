import logging
import time

from app.config import get_settings
from app.logging_setup import setup_logging


def main() -> None:
    setup_logging(get_settings().log_level)
    log = logging.getLogger("sentineliq.worker")
    log.info("worker started (Phase 2 placeholder, no jobs yet)")
    while True:
        time.sleep(30)
        log.info("worker heartbeat")


if __name__ == "__main__":
    main()
