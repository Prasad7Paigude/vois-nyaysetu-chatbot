# scripts/test_voice_chatbot.py

from voice_chatbot import VoiceChatbot

bot = VoiceChatbot()
result = bot.process(text_input="Explain FIR")

print("TEXT RESPONSE:")
print(result["text"])

print("\nAUDIO FILE:")
print(result["audio"])
