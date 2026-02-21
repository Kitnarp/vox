# voicecore/decorators.py
import sys

_registered_commands = {}

def command(phrase: str):
    """Decorator to register a function as a voice command handler."""
    def wrapper(func):
        module_name = func.__module__
        func_path = f"{module_name}.{func.__name__}"
        _registered_commands[phrase] = func_path
        return func
    return wrapper

def get_registered_commands():
    return _registered_commands