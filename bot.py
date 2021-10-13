import telebot
import random

from telebot import types

TOKEN = '2019972964:AAEGDvnyLPbdsB7MlQEFWiR2wTKFWvrGpDI'
words = ["аэропорт", "аквариум", "филармония", "нашатырь", "кастомизация", "интерактивный", "ассоциация",
         "эксплуатация", "машина", "коляска", "фракция", "ириска", "напалм", "экскурсия", "фунчоза", "картошка",
         "зоопарк", "задира", "карамель"]
rand_word = ""  # рандомное слово
list_letters = []  # список с буквами рандомного слова
list_lattice = []  # список с решетками
letter = ""  # случайно сгенерированная буква
attempts = 0  # попытки
rand_letter = ""  # рандомная буква
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать игру")
    item2 = types.KeyboardButton("Правила игры")
    item3 = types.KeyboardButton("Доступные слова")
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ бот, созданный для игры в поле чудес!"
                     .format(message.from_user, bot.get_me()), reply_markup=markup)


def start_game():
    global rand_word
    global list_letters
    global list_lattice
    global rand_letter
    rand_word = words[random.randint(0, 18)]

    for i in range(len(rand_word)):
        list_letters.insert(i, rand_word[i])
    for i in range(len(rand_word)):
        list_lattice.insert(i, "#")

    random_letter = random.randint(0, len(list_letters) - 1)

    list_lattice[random_letter] = list_letters[random_letter]


def delete_game():
    list_lattice.clear()
    list_letters.clear()

@bot.message_handler(func=lambda m: True)
def start_game_message(message):
    global rand_word
    global list_letters
    global list_lattice
    global attempts
    global rand_letter
    # начинаем игру
    if message.text == 'Начать игру':
        if rand_word == "":
            start_game()
            bot.send_message(message.chat.id, "Слово выбрано. " + ''.join(list_lattice))
        else:
            bot.send_message(message.chat.id, "Вы уже играете!")
    # правила игры
    elif message.text == 'Правила игры':
        bot.send_message(message.chat.id, "Загадывается рандомное слово. В первом раунде всегда "
                                          "открывается одна рандомная буква.\nУ вас есть 3 попытки, чтобы угадать "
                                          "букву. "
                                          "В четвертом раунде вы должны будете написать угаданное вами слово.\n"
                                          "Все буквы должны быть строчными")

    elif message.text == "Доступные слова":
        bot.send_message(message.chat.id, "Доступные слова: " + ', '.join(words))

    elif (len(message.text) > 1) & (rand_word == ""):
        bot.send_message(message.chat.id, "Я не знаю что ответить. Сначала начните игру!")

    elif rand_word == "":
        bot.send_message(message.chat.id, "Сначала начните игру!")

    else:
        # проверяем есть ли написанная буква в нашем слове
        if set(message.text).issubset(list_letters):
            if message.text == rand_word:
                bot.send_message(message.chat.id, "Вы выиграли!")
                attempts = 0
                rand_word = ""
                delete_game()
            else:
                if attempts == 3:
                    bot.send_message(message.chat.id, "Последняя попытка. Напишите слово!")
                elif attempts == 4:
                    bot.send_message(message.chat.id, " 4 попытки истрачены. Вы проиграли! Слово было: " + rand_word)
                    rand_word = ""
                    attempts = 0
                    delete_game()
                else:
                    attempts += 1
                    index = list_letters.index(message.text)
                    list_lattice[index] = message.text
                    bot.send_message(message.chat.id, "Правильно! " + ''.join(list_lattice))

        else:
            if attempts == 4:
                bot.send_message(message.chat.id, " 4 попытки истрачены. Вы проиграли! Слово было: " + rand_word)
                rand_word = ""
                attempts = 0
                delete_game()
            else:
                bot.send_message(message.chat.id, "Не правильно!!")
                if attempts == 3:
                     bot.send_message(message.chat.id, "Последняя попытка. Напишите слово!")
                attempts += 1


bot.polling()
