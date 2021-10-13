import telebot
import random

from telebot import types

TOKEN = '2019972964:AAEGDvnyLPbdsB7MlQEFWiR2wTKFWvrGpDI'
words = ["аэропорт", "аквариум", "филармония", "нашатырь", "кастомизация", "интерактивный", "ассоциация",
         "эксплуатация", "машина", "коляска", "фракция", "ириска", "напалм", "экскурсия", "фунчоза", "картошка",
         "зоопарк", "задира", "карамель"]
rand_word = ""  # рандомное слово
letters = []  # список с буквами рандомного слова
letters_game = []  # список с решетками
letter = ""  # случайно сгенерированная буква
attempts = 3  # попытки
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать игру")
    item2 = types.KeyboardButton("Правила игры")
    item3 = types.KeyboardButton("Начать заново")
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ бот, созданный для игры в поле чудес!"
                     .format(message.from_user, bot.get_me()), reply_markup=markup)


@bot.message_handler(func=lambda m: True)
def start_game_message(message):
    global rand_word
    global letters
    global letters_game
    global attempts

    if message.text == 'Начать игру':
        if rand_word == "":
            rand_word = words[random.randint(0, 18)]
            bot.send_message(message.chat.id, "Слово выбрано. " + rand_word)

            for i in range(len(rand_word)):
                letters.insert(i, rand_word[i])
            for i in range(len(rand_word)):
                letters_game.insert(i, "#")
        else:
            bot.send_message(message.chat.id, "Вы уже играете!")

    elif message.text == 'Правила игры':
        bot.send_message(message.chat.id, "Загадывается рандомное слово. В первом раунде всегда "
                                          "открывается одна рандомная буква.\nУ вас есть 2 попытки, чтобы угадать "
                                          "букву. "
                                          " В четвертом раунде вы должны будете написать угаданное вами слово")

    elif message.text == 'Начать заново':
        if rand_word == "":
            bot.send_message(message.chat.id, "Вы ещё не играете!")
        else:
            rand_word = words[random.randint(0, 18)]
            for i in range(len(rand_word)):
                letters.insert(i, rand_word[i])
            for i in range(len(rand_word)):
                letters_game.insert(i, "#")
            bot.send_message(message.chat.id, "Слово выбрано. " + rand_word)


# проверяем есть ли написанная буква в нашем слова
    elif rand_word != "":
        if set(message.text).issubset(letters):

            bot.send_message(message.chat.id, "Правильно!")
        else:
            bot.send_message(message.chat.id, "Не правильно!!")

    else:
        bot.send_message(message.chat.id, "Я не знаю что ответить :(")


bot.polling()
