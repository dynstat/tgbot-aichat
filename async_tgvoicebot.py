import asyncio  # Imports the asyncio library for writing single-threaded concurrent code using coroutines
import aiohttp  # Imports aiohttp for making asynchronous HTTP requests
import os  # Imports the os module to interact with the operating system
from dotenv import load_dotenv  # Imports load_dotenv to load environment variables from a .env file
load_dotenv()  # Loads environment variables from the .env file into the program's environment
from async_ai_voice import send_to_voice_AI  # Imports the send_to_voice_AI function from the async_ai_voice module

# Telegram Bot API setup
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Retrieves the Telegram bot token from environment variables
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"  # Constructs the base Telegram API URL using the bot token

async def get_voice_file(session, file_id):
    """
    Asynchronous function to retrieve the voice file from Telegram using the file ID.
    """
    # Get file path
    file_path_url = f"{TELEGRAM_API_URL}/getFile?file_id={file_id}"  # Constructs the URL to get file information from Telegram
    async with session.get(file_path_url) as response:  # Asynchronously sends a GET request to the file_path_url
        file_info = await response.json()  # Awaits and parses the JSON response containing file information
        file_path = file_info['result']['file_path']  # Extracts the file path from the response
    
    # Download file
    file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"  # Constructs the URL to download the actual voice file
    async with session.get(file_url) as response:  # Asynchronously sends a GET request to download the file
        return await response.read()  # Awaits and returns the raw bytes of the downloaded file

async def handle_message(session, message):
    """
    Asynchronous function to handle incoming Telegram messages.
    """
    if 'voice' in message:  # Checks if the incoming message contains a voice message
        file_id = message['voice']['file_id']  # Retrieves the file ID of the voice message
        audio_data = await get_voice_file(session, file_id)  # Awaits the retrieval of the audio data using the get_voice_file function
        transcription = await send_to_voice_AI(audio_data)  # Awaits the transcription of the audio data using the AI service
        
        # Send transcription back to user
        chat_id = message['chat']['id']  # Retrieves the chat ID to identify where to send the response
        text = transcription.get('text', 'Sorry, could not transcribe the audio due to AI error.')  # Gets the transcribed text or a default error message
        send_message_url = f"{TELEGRAM_API_URL}/sendMessage"  # Constructs the URL to send a message via the Telegram API
        payload = {
            'chat_id': chat_id,  # Specifies the chat ID where the message should be sent
            'text': text  # The transcribed text to send back to the user
        }
        await session.post(send_message_url, json=payload)  # Asynchronously sends a POST request to send the transcription back to the user