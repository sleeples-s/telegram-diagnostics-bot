import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import aiohttp

# Получаем токен из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("7904412826:AAEC2o47SmjqyiXzYUCXT7ZJKBW9WhdGg3o")

# Логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправьте мне текст или фото, и я попробую помочь с диагностикой.")

# Обработка текста
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id
    logger.info(f"[Text] From {user_id}: {user_text}")

    response = await query_ai_service(text=user_text)
    await update.message.reply_text(response)

# Обработка фото
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    photo_file = await update.message.photo[-1].get_file()
    photo_path = f"temp_{user_id}.jpg"
    await photo_file.download_to_drive(photo_path)
    logger.info(f"[Photo] From {user_id}: saved to {photo_path}")

    response = await query_ai_service(photo_path=photo_path)
    await update.message.reply_text(response)

    os.remove(photo_path)

# Мок AI-сервиса
async def query_ai_service(text=None, photo_path=None):
    if text:
        return "Диагностика текста: возможно, вы описали проблему с питанием устройства. Проверьте блок питания."
    elif photo_path:
        return "Диагностика фото: по изображению видно, что есть повреждение корпуса. Рекомендуется обратиться в сервис."
    return "Не удалось обработать запрос."

# Запуск
async def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения.")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Бот запущен...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
