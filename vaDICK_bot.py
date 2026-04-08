import logging
import re
import random
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8320879063:AAGhsHV--H_2u9qdJ3E87gUUNt5qElJ0GQs"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

JOKES = [
    "Идёт медведь по лесу, видит - машина горит. Сел в неё и сгорел!",
    "Встречаются два программиста: - Ты знаешь, я вчера всю ночь код писал. - И что? - Ничего, не скомпилировалось...",
    "Колобок повесился. Шерлок Холмс думает: \"Вот это поворот!\"",
]

# Инлайн-кнопки
keyboard = [
    [InlineKeyboardButton("🕐 Время", callback_data="time")],
    [InlineKeyboardButton("📅 Дата", callback_data="date")],
    [InlineKeyboardButton("😂 Анекдот", callback_data="joke")],
    [InlineKeyboardButton("🌤 Погода", callback_data="weather")],
    [InlineKeyboardButton("❓ Помощь", callback_data="help")],
    [InlineKeyboardButton("👋 Пока", callback_data="bye")]
]
reply_markup = InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я Вадик - твой помощник.\n\n"
        "Выбери действие:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Что я умею:\n\n"
        "📝 Считать примеры: 2+2, 10/3, 7*8\n"
        "😂 Анекдоты\n"
        "🕐 Время и дата\n"
        "🌤 Погода (например: погода Москва)\n\n"
        "Выбери действие на кнопках ниже 👇",
        reply_markup=reply_markup
    )

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(random.choice(JOKES), reply_markup=reply_markup)
    else:
        await update.message.reply_text(random.choice(JOKES), reply_markup=reply_markup)

async def show_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now()
    text = f"🕐 Сейчас {now.strftime('%H:%M:%S')}"
    if hasattr(update, 'callback_query'):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)

async def show_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now()
    text = f"📅 Сегодня {now.strftime('%d.%m.%Y')}"
    if hasattr(update, 'callback_query'):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if hasattr(update, 'callback_query'):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "🌍 Напиши город: /погода Москва\nНапример: погода Питер",
            reply_markup=reply_markup
        )
    else:
        if not context.args:
            await update.message.reply_text(
                "🌍 Напиши город: /погода Москва",
                reply_markup=reply_markup
            )
            return
        city = " ".join(context.args)
        await update.message.reply_text(
            f"🌤 Погода в {city}: +5°C, облачно",
            reply_markup=reply_markup
        )

async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if hasattr(update, 'callback_query'):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "👋 До встречи! Напиши /start чтобы вернуться",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "👋 До встречи! Напиши /start чтобы вернуться",
            reply_markup=reply_markup
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "time":
        now = datetime.datetime.now()
        await query.edit_message_text(f"🕐 Сейчас {now.strftime('%H:%M:%S')}", reply_markup=reply_markup)
    elif query.data == "date":
        now = datetime.datetime.now()
        await query.edit_message_text(f"📅 Сегодня {now.strftime('%d.%m.%Y')}", reply_markup=reply_markup)
    elif query.data == "joke":
        await query.edit_message_text(random.choice(JOKES), reply_markup=reply_markup)
    elif query.data == "weather":
        await query.edit_message_text(
            "🌍 Напиши город: /погода Москва\nНапример: погода Питер",
            reply_markup=reply_markup
        )
    elif query.data == "help":
        await query.edit_message_text(
            "🤖 Что я умею:\n\n"
            "📝 Считать примеры: 2+2, 10/3, 7*8\n"
            "😂 Анекдоты\n"
            "🕐 Время и дата\n"
            "🌤 Погода (например: погода Москва)\n\n"
            "Выбери действие на кнопках ниже 👇",
            reply_markup=reply_markup
        )
    elif query.data == "bye":
        await query.edit_message_text(
            "👋 До встречи! Напиши /start чтобы вернуться",
            reply_markup=reply_markup
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Математика
    if re.search(r'[\d\+\-\*/\(\)]', text):
        try:
            result = eval(text)
            await update.message.reply_text(f"🧮 Результат: {result}", reply_markup=reply_markup)
            return
        except:
            pass
    
    # Погода через текст
    if "погода" in text.lower():
        parts = text.lower().split()
        if len(parts) > 1:
            city = " ".join(parts[1:])
            await update.message.reply_text(f"🌤 Погода в {city}: +5°C, облачно", reply_markup=reply_markup)
            return
    
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
        answer = "До встречи! Напиши /start чтобы вернуться 👋"
    else:
        answer = f"Ты сказал: {text}\n\nВыбери действие на кнопках ниже 👇"
    
    await update.message.reply_text(answer, reply_markup=reply_markup)

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
    
    # Кнопки
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот Вадик запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
