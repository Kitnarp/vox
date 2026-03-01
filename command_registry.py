# command_registry.py

from config.logger_config import Command_registery

_registered_commands = {}

def command(*phrases):
    """
    Decorator to register a function as a voice command handler.
    Accepts:
      - A single string
      - A list/tuple of strings
      - Multiple string arguments (for convenience or by mistake)

    Example:
        @command("say hello")
        def greet(): ...

        @command(["play music", "start music"])
        def play_music(): ...

        @command("reload commands", "reload command")
        def reload_commands(): ...
    """
    # Normalize phrases into a flat list
    normalized = []
    for p in phrases:
        if isinstance(p, (list, tuple)):
            normalized.extend(p)
        elif isinstance(p, str):
            normalized.append(p)
        else:
            # Skip invalid types but don't crash
            Command_registery.error(f"Invalid command phrase type: {p!r}")
    
    def wrapper(func):
        module_name = func.__module__
        func_path = f"{module_name}.{func.__name__}"
        for phrase in normalized:
            _registered_commands[phrase] = func_path
        return func
    return wrapper


def get_registered_commands():
    """Return all registered commands as a dict."""
    return _registered_commands

def clear_registered_commands():
    """Clear all registered commands (used during reload)."""
    _registered_commands.clear()