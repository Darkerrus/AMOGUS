import telebot
import random

from telebot import types

TOKEN = '2019972964:AAEGDvnyLPbdsB7MlQEFWiR2wTKFWvrGpDI'

bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start'])
def send_welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать игру")
    item2 = types.KeyboardButton("Правила игры")
    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ бот, созданный для игры в поле чудес!"
                     .format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def start_game_message(message):
    if message.text == 'Начать игру':
        bot.send_message(message.chat.id, "Хорошо")
    elif message.text == 'Правила игры':
        bot.send_message(message.chat.id, "Загадывается рандомное слово на определенную тему. В первом раунде всегда "
                                          "открывается одна рандомная буква\nУ вас есть 2 попытки, чтобы угадать букву."
                                          " В четвертом раунде вы должны будете написать угаданное вами слово")
    else:
        bot.send_message(message.chat.id, "Я не знаю что ответить :(")


bot.polling()
