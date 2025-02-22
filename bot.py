import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

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


# Flask-приложение для вебхуков
app = Flask(__name__)


@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    """Обрабатывает запросы от Telegram через вебхук."""
    update = Update.de_json(request.get_json(), bot.application.bot)
    bot.application.update_queue.put_nowait(update)
    return "OK", 200


async def set_webhook():
    """Настраивает вебхук для Telegram."""
    await bot.application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")


def main():
    global bot
    bot = Application.builder().token(TOKEN).build()

    # Добавляем обработчик для новых участников
    bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_user))

    # Устанавливаем вебхук
    bot.loop.run_until_complete(set_webhook())

    # Запускаем Flask
    app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    main()
