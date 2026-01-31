import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

def callback(indata, frames, time, status):
    data_bytes = indata.tobytes()  # Convert NumPy buffer to raw bytes
    if rec.AcceptWaveform(data_bytes):
        print(json.loads(rec.Result()))
    else:
        print(json.loads(rec.PartialResult()))


with sd.InputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("Listening...")
    while True: 
        pass
    