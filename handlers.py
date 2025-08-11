from telebot import types
from config import BOT_TOKEN
from api import get_balance, deposit_to_user, payout_to_user
import telebot

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
user_data = {}

# === Start menyu ===
@bot.message_handler(commands=['start'])
def start_cmd(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💰 Hisob to‘ldirish", callback_data="deposit_menu"))
    markup.add(types.InlineKeyboardButton("💸 Yechish", callback_data="payout_menu"))
    markup.add(types.InlineKeyboardButton("📞 Aloqa", url="https://t.me/username"))
    bot.send_message(message.chat.id, "Kerakli amalni tanlang:", reply_markup=markup)

# === Hisob to‘ldirish menyusi ===
@bot.callback_query_handler(func=lambda call: call.data == "deposit_menu")
def deposit_menu(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("SpinBeter (UZS)", callback_data="deposit_spinbeter"))
    bot.edit_message_text("To‘ldirish turi:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# === Yechish menyusi ===
@bot.callback_query_handler(func=lambda call: call.data == "payout_menu")
def payout_menu(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("SpinBeter (UZS)", callback_data="payout_spinbeter"))
    bot.edit_message_text("Yechish turi:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# === Hisob to‘ldirish jarayoni ===
@bot.callback_query_handler(func=lambda call: call.data == "deposit_spinbeter")
def ask_deposit_id(call):
    bot.send_message(call.message.chat.id, "🆔 ID kiriting:")
    bot.register_next_step_handler(call.message, get_deposit_amount)

def get_deposit_amount(message):
    user_data[message.chat.id] = {"id": message.text}
    bot.send_message(message.chat.id, "💵 Summa kiriting:")
    bot.register_next_step_handler(message, confirm_deposit)

def confirm_deposit(message):
    user_data[message.chat.id]["amount"] = float(message.text)
    data = user_data[message.chat.id]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm_deposit"))
    bot.send_message(
        message.chat.id,
        f"📄 Ma'lumotlar:\n🆔 ID: {data['id']}\n💵 Summa: {data['amount']}",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "confirm_deposit")
def do_deposit(call):
    data = user_data.get(call.message.chat.id)
    res = deposit_to_user(int(data["id"]), data["amount"])
    bot.send_message(call.message.chat.id, f"Natija:\n{res}")

# === Yechish jarayoni ===
@bot.callback_query_handler(func=lambda call: call.data == "payout_spinbeter")
def ask_payout_id(call):
    bot.send_message(call.message.chat.id, "🆔 ID kiriting:")
    bot.register_next_step_handler(call.message, get_payout_code)

def get_payout_code(message):
    user_data[message.chat.id] = {"id": message.text}
    bot.send_message(message.chat.id, "🔢 Kod kiriting:")
    bot.register_next_step_handler(message, confirm_payout)

def confirm_payout(message):
    user_data[message.chat.id]["code"] = message.text
    data = user_data[message.chat.id]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm_payout"))
    bot.send_message(
        message.chat.id,
        f"📄 Ma'lumotlar:\n🆔 ID: {data['id']}\n🔢 Kod: {data['code']}",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "confirm_payout")
def do_payout(call):
    data = user_data.get(call.message.chat.id)
    res = payout_to_user(int(data["id"]), data["code"])
    bot.send_message(call.message.chat.id, f"Natija:\n{res}")

# === Balans komandasi (ixtiyoriy) ===
@bot.message_handler(commands=['balance'])
def balance_cmd(message):
    res = get_balance()
    bot.send_message(message.chat.id, f"💰 Balans: {res}")
