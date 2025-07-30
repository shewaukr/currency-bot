import telebot
from telebot import types
import requests
import json

bot = telebot.TeleBot("8265298834:AAGBaCd6UhcLmW_c-XvlLigsGc-k1cyuxWc")


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("💸 Ввести власну пару валют", callback_data="ownpare")
    markup.add(btn1)

    bot.send_message(message.chat.id, "Привіт, ось курс валют на сьогодні:")
    file = requests.get("https://v6.exchangerate-api.com/v6/83ac164789430ccd6d598706/latest/USD")
    data = json.loads(file.text)
    bot.send_message(message.chat.id, "Долар до Гривні: " + str(data["conversion_rates"]["UAH"]) + "\nДолар до Фунта: " + str(data["conversion_rates"]["GBP"]) + "\nДолар до Євра: " + str(data["conversion_rates"]["EUR"]) + "\nДолар до Єни: " + str(data["conversion_rates"]["JPY"]), reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
        if call.message:
            if call.data == "ownpare":
                msg = bot.send_message(call.message.chat.id, "Введіть валютну пару в форматі: USD/EUR")
                bot.register_next_step_handler(msg, ownPare)

def ownPare(message):
    try:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("💸 Ввести ще одну пару", callback_data="ownpare")
        markup.add(btn1)


        base = message.text.upper().split("/")
        target = base[1]
        file = requests.get(f"https://v6.exchangerate-api.com/v6/83ac164789430ccd6d598706/latest/{base[0]}")
        data = json.loads(file.text)
        bot.send_message(message.chat.id, f"Курс {base[0]} до {target}:  " + str(data["conversion_rates"][f"{target}"]), reply_markup=markup)
    except Exception:
        msg = bot.send_message(message.chat.id, "Такої валютної пари не існує aбо невірне написання, введіть будь ласка ще раз")
        bot.register_next_step_handler(msg, ownPare)

# bot.polling(none_stop=True)
