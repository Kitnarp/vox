# main.py
# temporary testing
from config.config import MODEL_PATH, MODEL_VOSK, COMMANDS_FILE
from voicecore.voice_manager import VoiceManager
from voicecore.vosk_recognizer import VoskRecognizer
from voicecore.features.command_feature import CommandFeature
import logging
import os


def main():
    print(logging.getLogger("voicecore").handlers)
    print(logging.getLogger().handlers)  # root logger
    # Path to your Vosk model (download separately and place in models/)
    model_path = os.path.join(MODEL_PATH, MODEL_VOSK)

    # Initialize recognizer (grammar phrases optional, freeform by default)
    # recognizer = VoskRecognizer(model_path)

    # Initialize features (CommandFeature for now)
    command_feature = CommandFeature(commands_file=COMMANDS_FILE)

    # Wire everything into the VoiceManager
    manager = VoiceManager(model_path=model_path, features=[command_feature])

    try:
        print("🎤 VoiceManager started. Speak a command!")
        manager.start()
    except KeyboardInterrupt:
        print("\n🛑 VoiceManager stopped.")
        manager.stop()
    while True:
        pass
if __name__ == "__main__":
    main()