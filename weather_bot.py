import os
import requests
import google.generativeai as genai

# 🔑 Load secrets from environment
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ⚙️ Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 💬 Prompt Gemini
prompt = """
Check the weather in San Antonio and Cypress, Texas,
and give me a short two-sentence summary like this:

In San Antonio: [weather description and temperature].
In Cypress: [weather description and temperature].
"""

# 🧠 Generate response
response = model.generate_content(prompt)
message = response.text.strip()

# 📤 Send to Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
requests.post(telegram_url, data=data)

print("✅ Message sent to Telegram!")
