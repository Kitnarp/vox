# voicecore/vosk_recognizer.py
import json
import os
from vosk import Model, KaldiRecognizer
from config.logger_config import recognizer_logger
from voicecore.base_recognizer import BaseRecognizer

class VoskRecognizer(BaseRecognizer):
    def __init__(self, model_path: str, samplerate: int = 16000, mode="grammar"):
        super().__init__(mode)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path not found: {model_path}")
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, samplerate)
        recognizer_logger.info(f"VoskRecognizer initialized (mode={self.mode}).")


    def process_audio(self, indata) -> str | None:
        data_bytes = indata.tobytes()
        if self.recognizer.AcceptWaveform(data_bytes):
            result = json.loads(self.recognizer.Result())
            text = result.get("text", "").strip() or None
            recognizer_logger.debug(f"Transcription: {text}")
            return text
        return None
    

    #TODO: Come up with a solution for vosk partial.get() sending the trailing words with each calls untill fully trancribed.
    def process_partial(self, indata) -> str | None:
        data_bytes = indata.tobytes()
        if not self.recognizer.AcceptWaveform(data_bytes):
            partial = json.loads(self.recognizer.PartialResult())
            text = partial.get("partial") or None
            if text:
                recognizer_logger.debug(f"Partial transcription: {text}")
            return text
        return None

    def reset(self):
        self.recognizer = KaldiRecognizer(self.model, self.recognizer.SampleRate())
        recognizer_logger.debug("Recognizer reset.")