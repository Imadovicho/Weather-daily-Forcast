import os
import requests

# Read API keys and chat ID from environment variables (GitHub Actions secrets)
OWM_API_KEY = os.environ.get("OWM_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not all([OWM_API_KEY, TELEGRAM_TOKEN, CHAT_ID]):
    raise ValueError("Please set OWM_API_KEY, TELEGRAM_TOKEN, and CHAT_ID as environment variables.")

cities = {
    "San Antonio": "San Antonio,US",
    "Cypress": "Cypress,US"
}

def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OWM_API_KEY}&units=metric"
    response = requests.get(url).json()

    # Basic error handling
    if response.get("cod") != 200:
        return "Weather data unavailable"

    weather_desc = response['weather'][0]['description'].capitalize()
    temp = round(response['main']['temp'])
    rain = response.get('rain', {}).get('1h', 0)
    rain_text = "with no rain expected" if rain == 0 else f"with {rain} mm rain expected"

    # Custom fog message for Cypress
    if "Cypress" in city_name:
        fog_message = " (though some earlier fog expected)"
        return f"{weather_desc}{fog_message}, reaching around {temp} °C, {rain_text}."

    return f"{weather_desc}, rising to about {temp} °C, {rain_text}."

# Build message
message = "Good morning! Here is the weather update:\n\n"
for city, name in cities.items():
    message += f"In {city}: {get_weather(name)}\n\n"

# Send message to Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
response = requests.get(telegram_url, params={"chat_id": CHAT_ID, "text": message})

if response.status_code == 200:
    print("Weather message sent successfully!")
else:
    print(f"Failed to send message: {response.text}")
