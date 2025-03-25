import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def tts(text: str) -> bytes:
    """
    Converts text to speech using a TTS service (e.g., OpenAI).

    Args:
        text: The text to convert to speech.

    Returns:
        bytes: The audio data in bytes (e.g., MP3).  Returns None on error.
    """
    try:
        # Replace this with your actual TTS API call (e.g., OpenAI)
        # This is just a placeholder for demonstration
        print(f"Generating TTS for: {text}")

        #Make sure you have your openAI API key.
        speech_file_path = "speech.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )

        response.stream_to_file(speech_file_path)

        with open(speech_file_path, "rb") as f:
            audio_data = f.read()

        os.remove(speech_file_path)

        return audio_data
        # Dummy data for testing without a real TTS service
        # return b"dummy audio data"  # Replace with actual audio bytes

    except Exception as e:
        print(f"Error in tts: {e}")
        return None