from flask import Flask, request
import telebot
from config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_URL
from handlers import bot

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return "Bot ishlayapti!", 200

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=10000)