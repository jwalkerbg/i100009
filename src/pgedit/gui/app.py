# gui/main.py

from ..core.config import Config
from ..logger import get_app_logger

logger = get_app_logger(__name__)

def run_gui_app(config:Config) -> None:

    try:
        logger.info("Running run_gui_app")
        logger.info("config = %s",str(config.config))

    finally:
        logger.info("Exiting run_gui_app")
