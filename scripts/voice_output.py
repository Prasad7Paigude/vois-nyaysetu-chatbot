# scripts/voice_output.py

import os
import uuid
from gtts import gTTS


class VoiceOutputProcessor:
    """
    Handles text-to-speech using gTTS.
    Simple, reliable fallback TTS.
    """

    def __init__(self, output_dir: str = "voice_outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def speak(self, text: str) -> str | None:
        """
        Converts text to speech and saves it as an MP3 file.
        Returns absolute file path on success, None on failure.
        """

        try:
            filename = f"{uuid.uuid4().hex}.mp3"
            filepath = os.path.abspath(os.path.join(self.output_dir, filename))

            tts = gTTS(text=text)
            tts.save(filepath)

            # Basic sanity check
            if not os.path.exists(filepath) or os.path.getsize(filepath) < 1000:
                return None

            return filepath

        except Exception:
            return None
