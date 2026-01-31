import sys
import os
import wave
import json
from vosk import Model, KaldiRecognizer

# Load model
model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

# Open audio file (must be WAV, mono, 16kHz)
wf = wave.open("test.wav", "rb")

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(json.loads(rec.Result()))

print(json.loads(rec.FinalResult()))
