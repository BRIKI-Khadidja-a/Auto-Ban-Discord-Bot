import logging
import os

def setup_logger():
    """Configure et retourne un logger configuré proprement pour le bot"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Crée un dossier 'logs' s'il n'existe pas
    log_file = os.path.join(log_dir, "bot.log")

    # Configuration du logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger("AutoBanBot")
    return logger
