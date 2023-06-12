import telebot
import requests
import time

from config import *
from baseword import BaseWord
from util import keyboard, bool_keyboard, reform, log

bot = telebot.TeleBot(TOKEN)


@log
@bot.message_handler(commands=['rules'])
def rules(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Привет! Сыграем в игру?', reply_markup=bool_keyboard())
    bot.register_next_step_handler(message, begin, set())


@log
@bot.message_handler()
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Привет! Сыграем в игру?', reply_markup=bool_keyboard())
    bot.register_next_step_handler(message, begin, set())


@log
def begin(message: telebot.types.Message, used_base_words):
    if message.text.lower() in ('да', 'конечно', 'давай', 'окей', 'играем', 'ага', 'дп', '/stop'):
        bot.send_message(message.chat.id, 'Отлично! Выбери уровень сложности', reply_markup=keyboard([EASY, NORMAL, HARD]))
        bot.register_next_step_handler(message, choose_level, used_base_words)
    else:
        bot.send_message(message.chat.id, 'Пиши в другой раз!')


@log
def choose_level(message: telebot.types.Message, used_base_words):
    if message.text not in (EASY, NORMAL, HARD):
        bot.send_message(message.chat.id, 'Выбери уровень сложности', reply_markup=keyboard([EASY, NORMAL, HARD]))
        bot.register_next_step_handler(message, choose_level, used_base_words)
        return

    base_word = BaseWord([EASY, NORMAL, HARD].index(message.text), used_base_words)
    used_base_words.add(base_word.word)
    bot_message = bot.send_message(message.chat.id,
                                   f'Найди {len(base_word.possible_words)} {reform("слово", len(base_word.possible_words))} в слове "{base_word.word.upper()}"')
    bot.pin_chat_message(message.chat.id, bot_message.id, disable_notification=True)
    time.sleep(1)
    bot.register_next_step_handler_by_chat_id(message.chat.id, trying, used_base_words, base_word, set())


@log
def trying(message: telebot.types.Message, used_base_words: set, base_word: BaseWord, trying_words: set):
    word = message.text.lower()
    if word == '/stop':
        begin(message, used_base_words)
        return

    if word in trying_words:
        bot.send_message(message.chat.id, 'Ты уже пробовал это слово')
        bot.register_next_step_handler(message, trying, used_base_words, base_word, trying_words)
        return
    trying_words.add(word)

    if word in base_word.set_of_all_words:
        if word in base_word.possible_words:
            base_word.possible_words.remove(word)
            ans = f'Да, ты нашёл слово! Слов осталось: {len(base_word.possible_words)}'
        elif all(word.count(i) <= base_word.word.count(i) for i in word) and word != base_word.word:
            base_word.possible_words.pop()
            ans = f'Да, ты нашёл слово! Слов осталось: {len(base_word.possible_words)}'
        else:
            ans = 'Нет, это слово не подходит'
    else:
        ans = 'Такого слова нет в словаре'

    if base_word.possible_words:
        bot.register_next_step_handler(message, trying, used_base_words, base_word, trying_words)
        bot.send_message(message.chat.id, ans)
    else:
        bot.register_next_step_handler(message, begin, used_base_words)
        bot.send_message(message.chat.id, 'Ты выиграл! Будешь играть ещё?', reply_markup=bool_keyboard())


if __name__ == '__main__':
    while 1:
        try:
            print('Start')
            # Запускаем бота
            bot.polling(non_stop=True, skip_pending=True)

        except Exception as log_error:
            if isinstance(log_error, requests.exceptions.ReadTimeout):
                # Такие ошибки могут появляться регулярно
                # Я читал, их возникновение связано с ошибками в библиотеке telebot
                print('That annoying errors erroring again')

            elif isinstance(log_error, requests.exceptions.ConnectionError):
                # Такое чаще всего при отсутствии подключения к интернету
                print('Ошибка соединения. Проверьте подключение к интернету')

            else:
                # Иначе отправляем админу, чтобы он разбирался
                print('Polling error: ' + f'({log_error.__class__}, {log_error.__cause__}): {log_error}')
            time.sleep(5)
