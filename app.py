import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Файл с приветствием
WELCOME_FILE = "welcome.txt"


def load_welcome_message():
    """Загружает приветственное сообщение из файла."""
    try:
        with open(WELCOME_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Привет, {name}! Добро пожаловать в чат!"


async def greet_user(update: Update, context):
    """Отправляет приветственное сообщение новому участнику."""
    welcome_message = load_welcome_message()

    for member in update.message.new_chat_members:
        await update.message.reply_text(welcome_message.format(name=member.full_name))


async def main():
    """Запускает Telegram-бота в режиме polling."""
    bot = Application.builder().token(TOKEN).build()

    # Добавляем обработчик для новых участников
    bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_user))

    print("Бот запущен!")

    # Запуск polling (бот сам проверяет обновления)
    await bot.run_polling()


# Запуск асинхронного цикла
if __name__ == '__main__':
    asyncio.run(main())
