# voicecore/dispatcher.py
import importlib
import json
import os
from config.logger_config import voice_logger

class Dispatcher:
    def __init__(self, commands_file="commands.json"):
        self.commands = {}
        if os.path.exists(commands_file):
            try:
                with open(commands_file, "r") as f:
                    self.commands = json.load(f)
                voice_logger.info(f"Dispatcher initialized with {len(self.commands)} commands.")
            except Exception as e:
                voice_logger.error(f"Failed to load commands file {commands_file}: {e}")
        else:
            voice_logger.warning(f"No commands file found at {commands_file}. Dispatcher initialized with empty command set.")

    def execute(self, text: str):
        """Find handler for recognized command and execute it."""
        if not self.commands:
            voice_logger.warning("No commands available. Please create commands.json.")
            return

        handler_path = self.commands.get(text)
        if not handler_path:
            voice_logger.warning(f"No handler found for command: {text}")
            return

        module_name, func_name = handler_path.rsplit(".", 1)
        try:
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
            func()
            voice_logger.info(f"Executed handler for command: {text}")
        except Exception as e:
            voice_logger.error(f"Error executing handler {handler_path}: {e}")
