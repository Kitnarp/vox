import sounddevice as sd
from config.logger_config import audio_logger

class AudioInput:
    def __init__(self, samplerate=16000, channels=1, device=None):
        self.samplerate = samplerate
        self.channels = channels
        self.device = device
        self.stream = None
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback
        audio_logger.debug("Audio callback set.")

    def start(self):
        if not self.callback:
            raise RuntimeError("Audio callback not set")
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype='int16',   # important: 16-bit PCM
            device=self.device,
            callback=self.callback,
            blocksize=8000
            )

        self.stream.start()
        audio_logger.info("Audio stream started.")

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            audio_logger.info("Audio stream stopped.")