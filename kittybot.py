"""Это бот, отправляющий котиков."""
import logging
import os

import requests
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()
token = os.getenv('TOKEN')
tim_id = os.getenv('tim_id')
URL = 'https://api.thecatapi.com/v1/images/search'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_new_image():
    """Получить картинку с котом."""
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    """Отправить нового кота."""
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def bot_writes_by_himself():
    """Функция самостоятельной отправки сообщений. Пока только автору."""
    bot = Bot(token=token)
    text = 'Вам телеграмма!'
    bot.send_message(tim_id, text)


def say_hi(update, context):
    """Бот здоровается."""
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я KittyBot!')


def wake_up(update, context):
    """Приветствие нового пользователя."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button,
    )
    context.bot.send_photo(chat.id, get_new_image())


def main():
    """Главная функция."""
    updater = Updater(token=token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
