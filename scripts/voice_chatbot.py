# scripts/voice_chatbot.py

import os

from rag_pipeline import answer_query
from voice_input import VoiceInputProcessor
from voice_output import VoiceOutputProcessor


class VoiceChatbot:
    """
    Orchestrates optional voice input and voice output
    around the core chatbot pipeline.
    """

    def __init__(self):
        self.voice_input = VoiceInputProcessor()
        self.voice_output = VoiceOutputProcessor()

    def process(
        self,
        text_input: str | None = None,
        audio_path: str | None = None
    ) -> dict:
        """
        Processes user input via text or voice.
        Returns a dict with text response and optional audio path.
        """

        # Step 1: Resolve input text
        if audio_path:
            transcribed = self.voice_input.transcribe(audio_path)
            if transcribed:
                text_input = transcribed

        if not text_input:
            return {
                "text": "Unable to process input.",
                "audio": None
            }

        # Step 2: Core chatbot response
        text_response = answer_query(text_input)

        # Step 3: Optional voice output
        audio_response = None

# Only generate audio if input was audio
        if audio_path:
            audio_response = self.voice_output.speak(text_response)


        return {
            "text": text_response,
            "audio": audio_response
        }
