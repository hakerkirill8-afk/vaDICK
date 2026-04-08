import logging
import re
import random
import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8320879063:AAGhsHV--H_2u9qdJ3E87gUUNt5qElJ0GQs"

logging.basicConfig(level=logging.INFO)

# Кнопки
buttons = ReplyKeyboardMarkup([
    ["🕐 Время", "📅 Дата"],
    ["😂 Анекдот", "❓ Помощь"]
], resize_keyboard=True)

# Анекдоты
JOKES = [
    "Идёт медведь по лесу, видит - машина горит. Сел в неё и сгорел!",
    "Встречаются два программиста: - Ты знаешь, я вчера всю ночь код писал. - И что? - Ничего, не скомпилировалось...",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Вадик - твой помощник.\n\n"
        "Просто пиши мне, или нажимай кнопки.\n"
        "Я понимаю: привет, как дела, примеры (2+2), анекдоты, время, дату.",
        reply_markup=buttons
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Что я умею:\n"
        "- Считать примеры (2+2)\n"
        "- Рассказывать анекдоты\n"
        "- Показывать время и дату (МСК)\n"
        "- Отвечать на привет, как дела, пока\n\n"
        "Просто напиши что-нибудь!",
        reply_markup=buttons
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Кнопки
    if text == "🕐 Время":
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        await update.message.reply_text(f"🕐 {now.strftime('%H:%M:%S')} (МСК)", reply_markup=buttons)
        return
    elif text == "📅 Дата":
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        await update.message.reply_text(f"📅 {now.strftime('%d.%m.%Y')}", reply_markup=buttons)
        return
    elif text == "😂 Анекдот":
        await update.message.reply_text(random.choice(JOKES), reply_markup=buttons)
        return
    elif text == "❓ Помощь":
        await help_command(update, context)
        return
    
    # Математика
    if re.search(r'[\d\+\-\*/\(\)]', text):
        try:
            result = eval(text)
            await update.message.reply_text(f"🧮 {result}", reply_markup=buttons)
            return
        except:
            pass
    
    # Обычное общение
    low = text.lower()
    if "привет" in low:
        await update.message.reply_text("Привет! Как дела? 😊", reply_markup=buttons)
    elif "как дела" in low:
        await update.message.reply_text("Отлично! А у тебя? 😎", reply_markup=buttons)
    elif "что делаешь" in low:
        await update.message.reply_text("Общаюсь с тобой! 🤔", reply_markup=buttons)
    elif "кто ты" in low:
        await update.message.reply_text("Я Вадик - помощник! 🤖", reply_markup=buttons)
    elif "спасибо" in low:
        await update.message.reply_text("Пожалуйста! 😊", reply_markup=buttons)
    elif "пока" in low:
        await update.message.reply_text("До встречи! 👋", reply_markup=buttons)
    else:
        await update.message.reply_text(f"Ты написал: {text}", reply_markup=buttons)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
