import telebot
from telebot import types

TOKEN = '2019972964:AAEGDvnyLPbdsB7MlQEFWiR2wTKFWvrGpDI'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, созданный для игры в поле чудес.")




bot.polling()
