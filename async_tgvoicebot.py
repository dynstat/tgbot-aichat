import asyncio
import aiohttp
import os
from dotenv import load_dotenv
load_dotenv()
from async_ai_voice import send_to_voice_AI




# Telegram Bot API setup
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

async def get_voice_file(session, file_id):
    # Get file path
    file_path_url = f"{TELEGRAM_API_URL}/getFile?file_id={file_id}"
    async with session.get(file_path_url) as response:
        file_info = await response.json()
        file_path = file_info['result']['file_path']
    
    # Download file
    file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
    async with session.get(file_url) as response:
        return await response.read()

async def handle_message(session, message):
    if 'voice' in message:
        file_id = message['voice']['file_id']
        audio_data = await get_voice_file(session, file_id)
        transcription = await send_to_voice_AI(audio_data)
        
        # Send transcription back to user
        chat_id = message['chat']['id']
        text = transcription.get('text', 'Sorry, could not transcribe the audio due to AI error.')
        send_message_url = f"{TELEGRAM_API_URL}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        await session.post(send_message_url, json=payload)

async def main():
    offset = 0
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                update_url = f"{TELEGRAM_API_URL}/getUpdates?offset={offset}&timeout=30"
                async with session.get(update_url) as response:
                    result = await response.json()
                
                if 'result' in result:
                    tasks = []
                    for update in result['result']:
                        offset = update['update_id'] + 1
                        message = update.get('message', {})
                        tasks.append(asyncio.create_task(handle_message(session, message)))
                    
                    await asyncio.gather(*tasks)
                else:
                    print(f"Unexpected API response: {result}")
                    await asyncio.sleep(5)  # Wait before retrying
            except aiohttp.ClientError as e:
                print(f"Error occurred: {e}")
                await asyncio.sleep(5)  # Wait before retrying
            except Exception as e:
                print(f"Unexpected error: {e}")
                await asyncio.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    asyncio.run(main())