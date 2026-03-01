from command_registry import command

@command(["hello", "say hello", "greeting", "greetings"])
def command_sayhello():
    print("Hello world!")