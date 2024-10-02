from fastapi import FastAPI, Request, Response  # Import FastAPI classes for creating the web app and handling requests/responses
from async_tgvoicebot import handle_message    # Import the asynchronous function to handle incoming Telegram messages
import aiohttp                                 # Import aiohttp for making asynchronous HTTP requests
import os                                      # Import os module to access environment variables

app = FastAPI()                                 # Initialize a FastAPI application instance

# Retrieve the Telegram bot token from environment variables
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
# Retrieve the secret token for webhook security from environment variables
SECRET_TOKEN = os.environ.get('SECRET_TOKEN')

@app.post("/webhook")
async def webhook(request: Request):
    """
    Endpoint to receive webhook updates from Telegram.
    Only processes the update if the secret token matches (if provided).
    """
    # Check if a secret token is set for additional security
    if SECRET_TOKEN:
        # Compare the secret token in the request headers with the expected SECRET_TOKEN
        if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != SECRET_TOKEN:
            # If tokens do not match, respond with 403 Forbidden status
            return Response(status_code=403)

    # Parse the incoming JSON payload from the request
    update = await request.json()
    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Call the handle_message function with the current session and the message part of the update
        await handle_message(session, update.get('message', {}))
    # Respond to Telegram that the update was received and processed successfully
    return {"status": "ok"}

@app.get("/")
async def root():
    """
    Root endpoint to confirm that the Telegram Bot is running.
    """
    # Return a simple JSON message indicating the bot's status
    return {"message": "Telegram Bot is running"}

# Endpoint to set webhook
@app.get("/set_webhook")
async def set_webhook():
    """
    Endpoint to set the Telegram webhook to the specified URL.
    This should be called after deploying the bot to ensure Telegram sends updates to the correct endpoint.
    """
    # Construct the webhook URL using the SPACE_ID environment variable
    webhook_url = f"https://{os.environ.get('SPACE_ID')}.hf.space/webhook"
    # Telegram API URL to set the webhook
    set_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    # Payload containing the webhook URL and the secret token for security
    payload = {
        "url": webhook_url,
        "secret_token": SECRET_TOKEN
    }
    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Send a POST request to Telegram's setWebhook API with the payload
        async with session.post(set_webhook_url, json=payload) as response:
            # Await and return the JSON response from Telegram confirming the webhook setup
            return await response.json()