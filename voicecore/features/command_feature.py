# voicecore/features/command_feature.py
from voicecore.dispatcher import Dispatcher
from config.logger_config import Command_logger
from .base_feature import BaseFeature

class CommandFeature(BaseFeature):
    def __init__(self, commands_file="commands.json"):
        self.dispatcher = Dispatcher(commands_file)
        Command_logger.info("CommandFeature initialized.")

    def handle_text(self, text: str):
        Command_logger.debug(f"CommandFeature received text: {text}")
        self.dispatcher.execute(text)
    
    def handle_partial(self, text):
        # Command_logger.debug(f"Doing partial...")
        return
