# scripts/voice_input.py

class VoiceInputProcessor:
    """
    Handles speech-to-text conversion using Whisper.
    Whisper is OPTIONAL and failures are silently ignored.
    """

    def __init__(self, model_size: str = "base"):
        self.model = None

        try:
            import whisper
            self.model = whisper.load_model(model_size)
        except Exception:
            # Whisper unavailable → voice input disabled
            self.model = None

    def transcribe(self, audio_path: str) -> str | None:
        """
        Transcribes an audio file to text.
        Returns None if transcription fails or Whisper is unavailable.
        """

        if not self.model:
            return None

        try:
            result = self.model.transcribe(audio_path)
            text = result.get("text", "").strip()
            return text if text else None
        except Exception:
            return None
