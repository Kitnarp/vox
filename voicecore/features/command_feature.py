# voicecore/features/command_feature.py
import re
from voicecore.dispatcher import Dispatcher
from config.logger_config import Command_logger
from .base_feature import BaseFeature

class CommandFeature(BaseFeature):
    def __init__(self, commands_file="commands.json"):
        self.dispatcher = Dispatcher(commands_file)
        Command_logger.info("CommandFeature initialized.")

    def handle_text(self, text: str):
        # Try to match text against known commands
        matched_phrase = self.match_command(text)
        if matched_phrase:
            Command_logger.debug(f"Matched command '{matched_phrase}' in text: {text}")
            self.dispatcher.execute(matched_phrase)
        else:
            Command_logger.debug(f"No command matched in text: {text}")

    def match_command(self, text: str) -> str | None:
        # Example: regex word-boundary matching
        for phrase in self.dispatcher._commands.keys():
            if re.search(rf"\b{re.escape(phrase)}\b", text):
                return phrase
        return None

    
    def handle_partial(self, text):
        # Command_logger.debug(f"Doing partial...")
        return
