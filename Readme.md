---
title: Telegram Voice Transcription Bot
emoji: 🎙️
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# Telegram Voice Transcription Bot

This Space hosts a Telegram bot that transcribes voice messages using the Hugging Face Whisper model.

## Setup

1. Set the following secrets in your Space's settings:
   - TELEGRAM_BOT_TOKEN
   - HUGGINGFACE_API_KEY
   - SECRET_TOKEN (for webhook security)
   - SPACE_ID (your Hugging Face Space ID)

2. After deploying, visit the `/set_webhook` endpoint to set up the webhook for your Telegram bot.