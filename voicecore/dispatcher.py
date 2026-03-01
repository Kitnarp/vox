# voicecore/dispatcher.py
import importlib
import json
import os
from config.config import COMMANDS_FILE
from voicecore.plugin_loader import load_plugins
from config.logger_config import Command_logger

class Dispatcher:
    # Shared command registry across all instances
    _commands = {}

    def __init__(self, commands_file=COMMANDS_FILE):
        self.commands_file = commands_file
        # Ensure commands are loaded once at startup
        if not Dispatcher._commands:
            self.reload()

    @classmethod
    def reload(cls):
        """Reload commands from JSON and plugins into the shared registry."""
        cls._commands.clear()

        # Load JSON commands
        if os.path.exists(COMMANDS_FILE):
            try:
                with open(COMMANDS_FILE, "r") as f:
                    json_cmds = json.load(f)
                cls._commands.update(json_cmds)
                Command_logger.info(f"Loaded {len(json_cmds)} commands from {COMMANDS_FILE}.")
            except Exception as e:
                Command_logger.error(f"Failed to load commands file {COMMANDS_FILE}: {e}")
        else:
            Command_logger.info("No commands.json found, skipping JSON commands.")

        # Load plugin commands
        try:
            plugin_cmds = load_plugins(reload=True)
            cls._commands.update(plugin_cmds)
            Command_logger.info(f"Loaded {len(plugin_cmds)} plugin commands.")
        except Exception as e:
            Command_logger.error(f"Failed to load plugin commands: {e}")

        Command_logger.info(f"Dispatcher registry now has {len(cls._commands)} total commands.")

    def execute(self, phrase: str):
        """Execute handler for a matched command phrase."""
        handler_path = Dispatcher._commands.get(phrase)
        if not handler_path:
            Command_logger.warning(f"No handler found for command: {phrase}")
            return

        module_name, func_name = handler_path.rsplit(".", 1)
        try:
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
            func()
            Command_logger.info(f"Executed handler for command: {phrase}")
        except Exception as e:
            Command_logger.error(f"Error executing handler {handler_path}: {e}")