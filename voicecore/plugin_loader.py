# voicecore/plugin_loader.py
import importlib
import pkgutil
import sys
import command_registry as command_registry

def load_plugins(plugin_package="plugins", reload=False):
    """
    Import all modules in the given package so their @command decorators run.
    If reload=True, force re-import of modules to pick up changes.
    """
    # Clear registry before reloading
    command_registry.clear_registered_commands()

    package = importlib.import_module(plugin_package)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_name = f"{plugin_package}.{module_name}"
        if reload and full_name in sys.modules:
            importlib.reload(sys.modules[full_name])
        else:
            importlib.import_module(full_name)

    return command_registry.get_registered_commands()