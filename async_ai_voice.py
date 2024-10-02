from transformers import pipeline
from typing import Dict, Any

# Initialize the transcription pipeline
transcriber = pipeline("automatic-speech-recognition", model="distil-whisper/distil-large-v3")

async def send_to_voice_AI(audio_data: bytes) -> Dict[str, Any]:
    """
    Transcribes audio data using the Hugging Face Whisper model.

    Args:
        audio_data (bytes): The raw audio data to be transcribed.

    Returns:
        Dict[str, Any]: A dictionary containing the transcription result or error message.
    """
    print("Transcribing audio")
    try:
        # Transcribe the audio
        result = transcriber(audio_data)
        return {"text": result["text"]}
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return {"text": "Sorry, an error occurred during transcription."}