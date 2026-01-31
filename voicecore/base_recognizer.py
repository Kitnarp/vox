# voicecore/base_recognizer.py
from abc import ABC, abstractmethod

class BaseRecognizer(ABC):
    def __init__(self, mode="freeform"):
        """
        mode: 'freeform' or 'command'
        """
        self.mode = mode

    def set_mode(self, mode: str):
        """Switch between freeform and command/grammar mode."""
        self.mode = mode

    @abstractmethod
    def process_audio(self, indata) -> str | None:
        """
        Process audio input and return recognized text depending on mode.
        Should return a final transcription (or command) if available.
        """
        pass

    def process_partial(self, indata) -> str | None:
        """
        Optional: return partial transcription if supported.
        Default implementation returns None, so recognizers like Whisper
        can ignore partials gracefully.
        """
        return None

    @abstractmethod
    def reset(self):
        """Reset recognizer state (e.g. reload grammar or clear buffers)."""
        pass
