from command_registry import command
from voicecore.dispatcher import Dispatcher


@command("reload commands", "reload command")
def reload_commands():
    dispatcher = Dispatcher()
    dispatcher.reload()
    print("------reloaded commands------")