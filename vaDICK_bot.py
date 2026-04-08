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
    "Колобок повесился. Шерлок Холмс думает: 'Вот это поворот!'",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Вадик - твой помощник.\n\n"
        "Просто пиши мне как другу, или нажимай кнопки.\n"
        "Я понимаю:\n"
        "- привет, как дела, что делаешь\n"
        "- кто ты, спасибо, пока\n"
        "- примеры (2+2, 10/3)\n\n"
        "Начни прямо сейчас!",
        reply_markup=buttons
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Что я умею:\n\n"
        "📝 Считать примеры (2+2, 10/3, 7*8)\n"
        "😂 Рассказывать анекдоты\n"
        "🕐 Показывать время и дату\n\n"
        "А ещё я понимаю:\n"
        "- Привет, как дела, что делаешь\n"
        "- Кто ты, спасибо, пока\n\n"
        "Просто напиши мне что-нибудь!",
        reply_markup=buttons
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Обработка кнопок
    if text == "🕐 Время":
        now = datetime.datetime.now()
        await update.message.reply_text(f"🕐 Сейчас {now.strftime('%H:%M:%S')}", reply_markup=buttons)
        return
    elif text == "📅 Дата":
        now = datetime.datetime.now()
        await update.message.reply_text(f"📅 Сегодня {now.strftime('%d.%m.%Y')}", reply_markup=buttons)
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
            await update.message.reply_text(f"🧮 Результат: {result}", reply_markup=buttons)
            return
        except:
            pass
    
    # Нормальное общение
    text_lower = text.lower()
    
    if "привет" in text_lower or "здравствуй" in text_lower:
        answer = "Привет! Как дела? 😊"
    elif "как дела" in text_lower:
        answer = "Отлично! А у тебя как? 😎"
    elif "что делаешь" in text_lower or "чем занят" in text_lower:
        answer = "Общаюсь с тобой! А ты что делаешь? 🤔"
    elif "кто ты" in text_lower or "как тебя зовут" in text_lower:
        answer = "Я Вадик - твой виртуальный помощник! 🤖"
    elif "спасибо" in text_lower:
        answer = "Пожалуйста! Всегда рад помочь 😊"
    elif "пока" in text_lower or "до свидания" in text_lower:
        answer = "До встречи! Буду ждать 👋"
    elif "молодец" in text_lower or "умница" in text_lower:
        answer = "Спасибо! Я стараюсь быть полезным 😊"
    elif "погода" in text_lower:
        answer = "Пока я не умею показывать погоду, но скоро научусь! 🌤"
    elif "имя" in text_lower:
        answer = "Тебя зовут как-то особенно? Расскажи! 📝"
    else:
        answer = f"Интересно... Расскажи подробнее! (Ты написал: {text})"
    
    await update.message.reply_text(answer, reply_markup=buttons)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот Вадик запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
