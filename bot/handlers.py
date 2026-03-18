from telegram import Update
from telegram.ext import ContextTypes

from bot.rag import generate_answer

START_TEXT = (
    "Привет! Я ИИ-консультант по теме искусственного интеллекта "
    "и промпт-инжиниринга.\n\n"
    "Задайте мне любой вопрос, и я постараюсь помочь!"
)

HELP_TEXT = (
    "Просто напишите свой вопрос текстом, и я отвечу.\n\n"
    "Примеры вопросов:\n"
    "• Что такое RAG?\n"
    "• Как работает промпт-инжиниринг?\n"
    "• Что такое эмбеддинги?"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.chat.send_action("typing")

    try:
        answer = generate_answer(query)
    except Exception as e:
        answer = f"Произошла ошибка при обработке запроса: {e}"

    await update.message.reply_text(answer)
