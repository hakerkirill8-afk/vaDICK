import logging
import re
import random
import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8320879063:AAGhsHV--H_2u9qdJ3E87gUUNt5qElJ0GQs"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

JOKES = [
    "Идёт медведь по лесу, видит - машина горит. Сел в неё и сгорел!",
    "Встречаются два программиста: - Ты знаешь, я вчера всю ночь код писал. - И что? - Ничего, не скомпилировалось...",
]

# Клавиатура с кнопками
menu_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("🕐 Время"), KeyboardButton("📅 Дата")],
    [KeyboardButton("😂 Анекдот"), KeyboardButton("❓ Помощь")],
    [KeyboardButton("👋 Пока")]
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Вадик. Выбери действие:",
        reply_markup=menu_keyboard
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я умею:\n"
        "- Считать примеры (2+2)\n"
        "- Показывать время и дату\n"
        "- Рассказывать анекдоты\n\n"
        "Просто нажми на кнопку!",
        reply_markup=menu_keyboard
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🕐 Время":
        now = datetime.datetime.now()
        await update.message.reply_text(f"Сейчас {now.strftime('%H:%M:%S')}", reply_markup=menu_keyboard)
    elif text == "📅 Дата":
        now = datetime.datetime.now()
        await update.message.reply_text(f"Сегодня {now.strftime('%d.%m.%Y')}", reply_markup=menu_keyboard)
    elif text == "😂 Анекдот":
        await update.message.reply_text(random.choice(JOKES), reply_markup=menu_keyboard)
    elif text == "❓ Помощь":
        await help_command(update, context)
    elif text == "👋 Пока":
        await update.message.reply_text("До встречи! Напиши /start чтобы вернуться", reply_markup=menu_keyboard)
    else:
        # Обычный текст — считаем примеры или просто отвечаем
        if re.search(r'[\d\+\-\*/\(\)]', text):
            try:
                result = eval(text)
                await update.message.reply_text(f"Результат: {result}", reply_markup=menu_keyboard)
                return
            except:
                pass
        await update.message.reply_text(f"Ты написал: {text}", reply_markup=menu_keyboard)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    
    print("Бот Вадик запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
