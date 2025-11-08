import os
import requests

# Read API keys and chat ID from environment variables (GitHub Actions secrets)
OWM_API_KEY = os.environ.get("OWM_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not all([OWM_API_KEY, TELEGRAM_TOKEN, CHAT_ID]):
    raise ValueError("Please set OWM_API_KEY, TELEGRAM_TOKEN, and CHAT_ID as environment variables.")

# Cities with coordinates
cities = {
    "San Antonio": {"lat": 29.4241, "lon": -98.4936},
    "Cypress": {"lat": 29.9699, "lon": -95.6639}
}

def get_weather(city_info):
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?lat={city_info['lat']}&lon={city_info['lon']}&appid={OWM_API_KEY}&units=metric"
    )
    response = requests.get(url).json()

    # Debugging: uncomment to see full API response
    # print(response)

    # Handle API errors
    if response.get("cod") != 200:
        return "Weather data unavailable."

    weather_desc = response['weather'][0]['description'].capitalize()
    temp = round(response['main']['temp'])
    rain = response.get('rain', {}).get('1h', 0)
    rain_text = "with no rain expected" if rain == 0 else f"with {rain} mm rain expected"

    # Special fog message for Cypress
    if city_info['lat'] == 29.9699:  # Cypress
        fog_text = " (though some earlier fog expected)"
        return f"{weather_desc}{fog_text}, reaching around {temp} °C, and also {rain_text}."
    else:
        return f"{weather_desc}, rising to about {temp} °C, {rain_text}."

# Build dynamic message
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
