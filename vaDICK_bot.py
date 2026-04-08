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
    "Колобок повесился. Шерлок Холмс думает: \"Вот это поворот!\"",
]

# Кнопки
buttons = ReplyKeyboardMarkup([
    [KeyboardButton("🕐 Время"), KeyboardButton("📅 Дата")],
    [KeyboardButton("😂 Анекдот"), KeyboardButton("🌤 Погода")],
    [KeyboardButton("❓ Помощь"), KeyboardButton("👋 Пока")]
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я Вадик - твой помощник.\n\n"
        "Нажми на кнопку или напиши команду:",
        reply_markup=buttons
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Что я умею:\n\n"
        "📝 Считать примеры: 2+2, 10/3, 7*8\n"
        "😂 Анекдоты — кнопка или /анекдот\n"
        "🕐 Время и дата — кнопка или /время\n"
        "🌤 Погода — кнопка или /погода Москва\n\n"
        "Просто напиши мне что-нибудь!",
        reply_markup=buttons
    )

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(JOKES), reply_markup=buttons)

async def show_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now()
    await update.message.reply_text(
        f"🕐 Сейчас {now.strftime('%H:%M:%S')}\n📅 Сегодня {now.strftime('%d.%m.%Y')}",
        reply_markup=buttons
    )

async def show_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now()
    await update.message.reply_text(
        f"📅 Сегодня {now.strftime('%d.%m.%Y')}",
        reply_markup=buttons
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🌍 Напиши город: /погода Москва\nИли: погода Питер",
            reply_markup=buttons
        )
        return
    city = " ".join(context.args)
    await update.message.reply_text(
        f"🌤 Погода в {city}: +5°C, облачно",
        reply_markup=buttons
    )

async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 До встречи! Буду ждать твоих сообщений!",
        reply_markup=buttons
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Обработка кнопок
    if text == "🕐 Время":
        await show_time(update, context)
        return
    elif text == "📅 Дата":
        await show_date(update, context)
        return
    elif text == "😂 Анекдот":
        await joke(update, context)
        return
    elif text == "🌤 Погода":
        await update.message.reply_text(
            "🌍 Напиши город: /погода Москва",
            reply_markup=buttons
        )
        return
    elif text == "❓ Помощь":
        await help_command(update, context)
        return
    elif text == "👋 Пока":
        await bye(update, context)
        return
    
    # Математика
    if re.search(r'[\d\+\-\*/\(\)]', text):
        try:
            result = eval(text)
            await update.message.reply_text(f"🧮 Результат: {result}", reply_markup=buttons)
            return
        except:
            pass
    
    # Простые ответы
    text_lower = text.lower()
    if "привет" in text_lower:
        answer = "Привет! Как дела?"
    elif "как дела" in text_lower:
        answer = "Отлично! А у тебя?"
    elif "кто ты" in text_lower:
        answer = "Я Вадик - твой помощник!"
    elif "спасибо" in text_lower:
        answer = "Пожалуйста! Всегда рад помочь 😊"
    elif "пока" in text_lower:
        answer = "До встречи! Буду ждать 👋"
    else:
        answer = f"Ты сказал: {text}"
    
    await update.message.reply_text(answer, reply_markup=buttons)

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("анекдот", joke))
    app.add_handler(CommandHandler("time", show_time))
    app.add_handler(CommandHandler("время", show_time))
    app.add_handler(CommandHandler("date", show_date))
    app.add_handler(CommandHandler("дата", show_date))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("погода", weather))
    app.add_handler(CommandHandler("bye", bye))
    app.add_handler(CommandHandler("пока", bye))
    
    # Сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот Вадик запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
