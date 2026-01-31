import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import subprocess

# Load Vosk model
model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

# Define your voice commands and scripts
commands = {
    "open": r"C:\Windows\System32\calc.exe",
    "run ahk script": r"E:\_Scripts\AutoHotkey\myscript.ahk",
    "launch python": r"python E:\_Scripts\PYTHON\myscript.py"
}

def callback(indata, frames, time, status):
    data_bytes = indata.tobytes()
    if rec.AcceptWaveform(data_bytes):
        result = json.loads(rec.Result())
        text = result.get("text", "").lower()
        print("Recognized:", text)

        # Check if recognized text matches a command
        for phrase, script in commands.items():
            if phrase in text:
                print(f"Executing: {script}")
                subprocess.Popen(script, shell=True)

with sd.InputStream(samplerate=16000, blocksize=8000, dtype='int16',
                    channels=1, callback=callback):
    print("Listening for commands...")
    while True:
        pass
