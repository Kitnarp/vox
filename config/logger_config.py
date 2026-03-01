import logging
import os

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    """Create a logger with its own file handler."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # prevent bubbling up to parent loggers

    # Avoid duplicate handlers if called multiple times
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        fh = logging.FileHandler(os.path.join(LOG_DIR, log_file))
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Also log to console for debugging
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

# Profiles

# Core Profiles
server_logger = setup_logger("server", "server.log", logging.DEBUG)
voice_logger = setup_logger("voicecore", "voicecore.log", logging.DEBUG)
audio_logger = setup_logger("voicecore.audio", "audioinput.log", logging.DEBUG)
recognizer_logger = setup_logger("voicecore.recognizer", "recognizer.log")

# Command Registery
Command_registery = setup_logger("Registery", "Registery.log", logging.DEBUG) 

# feature Profiles
Command_logger = setup_logger("feature.command", "command_feature.log", logging.DEBUG)
