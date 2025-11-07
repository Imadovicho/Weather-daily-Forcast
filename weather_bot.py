import os
import requests

# Read API keys and chat ID from environment variables (GitHub Actions secrets)
OWM_API_KEY = os.environ.get("OWM_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not all([OWM_API_KEY, TELEGRAM_TOKEN, CHAT_ID]):
    raise ValueError("Please set OWM_API_KEY, TELEGRAM_TOKEN, and CHAT_ID as environment variables.")

# Cities to check
cities = {
    "San Antonio": {"name": "San Antonio", "country": "US"},
    "Cypress": {"name": "Cypress", "country": "US"}
}

def get_weather(city_info):
    city_name = f"{city_info['name']},{city_info['country']}"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OWM_API_KEY}&units=metric"
    response = requests.get(url).json()

    # Handle API errors
    if response.get("cod") != 200:
        return "Weather data unavailable."

    weather_main = response['weather'][0]['main']
    weather_desc = response['weather'][0]['description'].capitalize()
    temp = round(response['main']['temp'])
    rain = response.get('rain', {}).get('1h', 0)

    # Determine rain message
    rain_text = "with no rain expected" if rain == 0 else f"with {rain} mm rain expected"

    # Custom fog message for Cypress if weather is clear and early fog is likely
    fog_text = ""
    if city_info['name'] == "Cypress" and weather_main.lower() in ["clear", "sunny"]:
        fog_text = " (though some earlier fog expected)"

    # Format dynamic message
    if city_info['name'] == "Cypress":
        return f"{weather_desc}{fog_text}, reaching around {temp} °C, and also {rain_text}."
    else:
        return f"{weather_desc}, rising to about {temp} °C, {rain_text}."

# Build message
message = ""
for city, info in cities.items():
    message += f"In {city}: {get_weather(info)}\n"

# Send message to Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
response = requests.get(telegram_url, params={"chat_id": CHAT_ID, "text": message})

if response.status_code == 200:
    print("Weather message sent successfully!")
else:
    print(f"Failed to send message: {response.text}")
