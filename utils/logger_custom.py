import logging
import os
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal

class LoggerSignals(QObject):
    """Signal pour envoyer les logs vers le QTextBrowser de la UI."""
    new_log = pyqtSignal(str, str) # (Message, Niveau)

class CyberLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.signals = LoggerSignals()
        self._ensure_dir()
        
        # Fichier log par jour
        log_file = os.path.join(self.log_dir, f"sentinel_{datetime.now().strftime('%Y-%m-%d')}.log")
        
        self.logger = logging.getLogger("CyberSentinel")
        self.logger.setLevel(logging.DEBUG)
        
        # Formatage pour le fichier texte
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%H:%M:%S')
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _ensure_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def info(self, msg):
        self.logger.info(msg)
        self.signals.new_log.emit(msg, "INFO")

    def error(self, msg):
        self.logger.error(msg)
        self.signals.new_log.emit(msg, "ERROR")

    def warning(self, msg):
        self.logger.warning(msg)
        self.signals.new_log.emit(msg, "WARNING")

# On crée une instance unique pour tout le projet
cyber_log = CyberLogger()