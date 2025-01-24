# gui/main.py

import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from ..core.config import Config
from ..logger import get_app_logger

logger = get_app_logger(__name__)

def run_gui_app(config:Config) -> int:

    try:
        logger.info("Running run_gui_app")
        logger.info("config = %s",str(config.config))
        app = QGuiApplication(sys.argv)
        engine = QQmlApplicationEngine()
        qml_file = Path(__file__).resolve().parent / "main.qml"
        engine.load(qml_file)
        if not engine.rootObjects():
            return -1
        return app.exec()

    finally:
        logger.info("Exiting run_gui_app")
