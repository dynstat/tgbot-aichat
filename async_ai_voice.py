import aiohttp
import os
import json
from typing import Dict, Any

API_URL = "https://api-inference.huggingface.co/models/distil-whisper/distil-large-v3"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

async def send_to_voice_AI(audio_data: bytes) -> Dict[str, Any]:
    print("Sending to voice AI")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(API_URL, headers=headers, data=audio_data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    error_json = json.loads(error_text)
                    return {
                        "text": f"error: {error_json.get('error', 'Unknown error')}\n"
                                f"Estimated time to load: {error_json.get('estimated_time', 'unknown')} seconds"
                    }
        except aiohttp.ClientError as e:
            return {"text": f"Network error: {str(e)}"}
        except json.JSONDecodeError:
            return {"text": "Error: Unable to parse API response"}

# Example usage:
# import asyncio
# async def example():
#     with open("sample1.flac", "rb") as f:
#         audio_data = f.read()
#     output = await send_to_voice_AI(audio_data)
#     print(output)
# asyncio.run(example())