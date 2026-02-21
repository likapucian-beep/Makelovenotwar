import os
from flask import Flask, request
from telegram import Bot
from openai import OpenAI

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    
    if "message" not in data:
        return "OK"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Odpovídej česky, lehce ironicky."},
            {"role": "user", "content": text}
        ]
    )

    reply = response.choices[0].message.content
    bot.send_message(chat_id=chat_id, text=reply)

    return "OK"

if __name__ == "__main__":
    app.run()
