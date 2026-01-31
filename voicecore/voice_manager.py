# voicecore/voice_manager.py
from config.logger_config import voice_logger
from config.logger_config import audio_logger
from voicecore.audio_input import AudioInput
from voicecore.vosk_recognizer import VoskRecognizer
# from voicecore.whisper_recognizer import WhisperRecognizer  # future

class VoiceManager:
    def __init__(self, recognizer=None, features=None, model_path="models/vosk-model-small-en-us-0.15"):
        self.audio = AudioInput()
        self.recognizer = recognizer or VoskRecognizer(model_path)
        self.features = features or []
        self.audio.set_callback(self._audio_callback)
        voice_logger.info("VoiceManager initialized.")

    def _audio_callback(self, indata, frames, time, status):
        if status:
            audio_logger.warning(f"Audio status: {status}")
        # audio_logger.debug(f"Frames={frames}, dtype={indata.dtype}, shape={indata.shape}")

        partial_text = self.recognizer.process_partial(indata)
        if partial_text:
            for feature in self.features:
                feature.handle_partial(partial_text)

        text = self.recognizer.process_audio(indata)
        if text:
            for feature in self.features:
                feature.handle_text(text)

    def add_feature(self, feature):
        self.features.append(feature)
        voice_logger.info(f"Feature {feature.__class__.__name__} added.")

    def set_recognizer(self, recognizer_name, **kwargs):
        """Swap recognizer on the fly based on user-friendly name."""
        if recognizer_name == "vosk":
            self.recognizer = VoskRecognizer(kwargs.get("model_path", "models/vosk-model-small-en-us-0.15"))
            voice_logger.info("Switched recognizer to Vosk.")
        elif recognizer_name == "whisper":
            # self.recognizer = WhisperRecognizer(kwargs.get("model_size", "small"))
            #voice_logger.info("Switched recognizer to Whisper.")
            voice_logger.warning("Not implemented yet!!")
        else:
            voice_logger.error(f"Unknown recognizer: {recognizer_name}")

    def start(self):
        self.audio.start()
        voice_logger.info("VoiceManager started.")

    def stop(self):
        self.audio.stop()
        voice_logger.info("VoiceManager stopped.")