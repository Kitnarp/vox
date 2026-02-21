from voicecore.decorators import command

@command("hello")
def greet():
    print("Hello world!!!")

