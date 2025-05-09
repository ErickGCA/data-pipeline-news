import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(name: str, log_level: str = "INFO") -> logging.Logger:
    """
    Configura e retorna um logger formatado.
    
    Args:
        name: Nome do logger
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        logging.Logger: Logger configurado
    """
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    level = log_levels.get(log_level.upper(), logging.INFO)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        if os.getenv("LOG_TO_FILE", "False").lower() == "true":
            log_dir = Path(__file__).resolve().parent.parent.parent / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            
            today = datetime.now().strftime("%Y-%m-%d")
            log_file = log_dir / f"{name}_{today}.log"
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    return logger 