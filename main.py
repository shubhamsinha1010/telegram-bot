import requests
import openai
from telegram.ext import Application, CommandHandler
import os
from dotenv import load_dotenv
load_dotenv()

# Initial message context for ChatGPT
messages = [{"role": "system", "content": "You are an intelligent assistant."}]
openai.api_key = os.environ.get("OPENAI_API_KEY")
# Function to get weather data from OpenWeatherMap API
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={os.environ.get('TELEGRAM_API_KEY')}&q={city}"
    response = requests.get(url)
    data = response.json()

    # Get temperature in Celsius
    temp = data.get("main", {}).get("temp")
    if isinstance(temp, (int, float)):
        temp = round(temp - 273.15, 2)  # Convert from Kelvin to Celsius
        return f"The current temperature in {city} is {temp}° Celsius."
    else:
        return "Temperature Unavailable at the moment. Please check the city name."

# Function to interact with ChatGPT
def ask_chatgpt(prompt):
    if prompt:
        messages.append({"role": "user", "content": prompt})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        return reply

# /start command handler
async def start(update, context):
    await update.message.reply_text("Send me a city name, and I'll tell you the temperature. Use /weather <city> or ask a question with /askchatgpt <prompt>.")

# /weather command handler
async def get_weather_command(update, context):
    if len(context.args) < 1:
        await update.message.reply_text("Please provide a city name, e.g., /weather Ahmedabad.")
        return

    city = context.args[0]
    weather = get_weather(city)
    await update.message.reply_text(weather)

# /askchatgpt command handler
async def get_chatgpt_command(update, context):
    if len(context.args) < 1:
        await update.message.reply_text("Please provide a question, e.g., /askchatgpt What's the capital of France?")
        return

    prompt = " ".join(context.args)
    answer = ask_chatgpt(prompt)
    await update.message.reply_text(answer)

# Main function to initialize the bot and set up handlers
def main():
    print("Starting Bot...")

    # Initialize the application with the bot token
    application = Application.builder().token(os.environ.get('BOT_TOKEN')).build()

    # Add command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('weather', get_weather_command))
    application.add_handler(CommandHandler('askchatgpt', get_chatgpt_command))

    # Start the bot
    application.run_polling()

# Entry point
if __name__ == '__main__':
    main()
