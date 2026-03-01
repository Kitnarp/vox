from command_registry import command

# for low level keysends
import win32api
import win32con


@command(["pause", "resume", "music"])
def pauses():
    # Virtual key code for Play/Pause media
    VK_MEDIA_PLAY_PAUSE = 0xB3
    # Send Play/Pause
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0, 0)   # key down
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, win32con.KEYEVENTF_KEYUP, 0)   # key up
    print("Play/Pause sent without blocking")

