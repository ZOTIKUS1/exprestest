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

# Функция для загрузки приветственного сообщения из текстового файла
def load_welcome_message(chat_title: str):
    """Загружает приветственное сообщение из текстового файла."""
    try:
        # Преобразуем chat_title, чтобы сделать название файла
        file_name = f"{chat_title}.txt"
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        # Если файл не найден, возвращаем стандартное сообщение
        return f"Привет, {{name}}! Добро пожаловать в чат '{chat_title}'!"

async def greet_user(update: Update, context):
    """Отправляет приветственное сообщение новому участнику в зависимости от чата."""
    chat_title = update.message.chat.title.lower()  # Преобразуем в нижний регистр для обработки
    
    # Приветственные сообщения для каждого чата
    if chat_title == "info":
        welcome_message = load_welcome_message("info")
    elif chat_title == "play":
        welcome_message = load_welcome_message("play")
    elif chat_title == "го гулять":
        welcome_message = load_welcome_message("го_гулять")
    elif chat_title == "базар":
        welcome_message = load_welcome_message("базар")
    else:
        welcome_message = load_welcome_message("welcome")  # Это для чатов, которые не попали в условия

    # Отправляем приветственное сообщение для каждого нового участника
    for member in update.message.new_chat_members:
        await update.message.reply_text(welcome_message.format(name=member.full_name))


async def run_bot():
    """Запускает бота."""
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_user))

    print("Бот запущен!")

    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()

    # Держим бота активным
    await asyncio.Event().wait()


# Запуск бота
if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(run_bot())  # Запуск без закрытия loop
    except RuntimeError:
        loop.create_task(run_bot())  # Если loop уже работает, создаём задачу
