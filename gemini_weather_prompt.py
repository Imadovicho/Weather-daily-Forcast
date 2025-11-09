import os
import requests
import google.generativeai as genai

# 🔑 Load secrets from GitHub Actions
GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not GEMINI_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY environment variable!")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Prompt for Gemini
prompt = """
Check today’s weather in San Antonio and Cypress, Texas.
Give me a short, two-sentence summary in this style:

In San Antonio: [weather description, highest temperature today, and if there is rain or wind].
In Cypress: [weather description, highest temperature today, and if there is rain or wind].
"""

# Generate response from Gemini
response = model.generate_content(prompt)
message = response.text.strip()

# Send message to Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
requests.post(telegram_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

print("✅ Message sent to Telegram!")
print(message)
