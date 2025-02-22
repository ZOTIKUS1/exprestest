import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Ошибка: BOT_TOKEN не найден! Проверь .env файл или Secrets в Replit.")

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


async def run_bot():
    """Запускает бота, не закрывая event loop в Replit."""
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_user))

    print("Бот запущен!")

    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()

    # Держим бота активным (loop.run_forever() нельзя в Replit)
    await asyncio.Event().wait()


# Запуск без конфликта с Replit
if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(run_bot())  # Запуск без закрытия loop
    except RuntimeError:
        loop.create_task(run_bot())  # Если loop уже работает, создаём задачу
