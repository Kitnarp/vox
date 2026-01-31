from vosk import Model, KaldiRecognizer
import json
import os
from config.logger_config import recognizer_logger

class Recognizer:
    def __init__(self, model_path: str, samplerate: int = 16000):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path not found: {model_path}")
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, samplerate)
        recognizer_logger.info(f"Recognizer initialized with model at {model_path}")

    def process_audio(self, indata) -> str | None:
        """Process raw audio input and return recognized text if available."""
        if self.recognizer.AcceptWaveform(indata):
            result = json.loads(self.recognizer.Result())
            text = result.get("text", "").strip()
            if text:
                recognizer_logger.debug(f"Recognized text: {text}")
                return text
        else:
            partial = json.loads(self.recognizer.PartialResult())
            if partial.get("partial"):
                recognizer_logger.debug(f"Partial recognition: {partial['partial']}")
        return None

    def reset(self):
        """Reset recognizer state."""
        self.recognizer = KaldiRecognizer(self.model, self.recognizer.SampleRate())
        recognizer_logger.debug("Recognizer reset.")