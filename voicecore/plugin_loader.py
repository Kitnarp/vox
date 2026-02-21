# voicecore/plugin_loader.py
import importlib
import pkgutil
import voicecore.decorators as decorators

def load_plugins(plugin_package="plugins"):
    """
    Import all modules in the given package (e.g. 'plugins') so their
    @command decorators run and register handlers.
    """
    package = importlib.import_module(plugin_package)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{plugin_package}.{module_name}")
    return decorators.get_registered_commands()