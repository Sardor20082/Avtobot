import os
from flask import Flask, request
import telebot
from config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_URL
from handlers import bot  # handlers.py ichida bot = telebot.TeleBot(BOT_TOKEN) bo'lishi kerak

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot ishlayapti!", 200

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    print("Webhook update:", json_str)  # Log uchun
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)
