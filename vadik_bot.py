import logging
import re
import random
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "ТВОЙ_ТОКЕН_СЮДА"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

JOKES = [
    "Идёт медведь по лесу, видит - машина горит. Сел в неё и сгорел!",
    "Встречаются два программиста: - Ты знаешь, я вчера всю ночь код писал. - И что? - Ничего, не скомпилировалось...",
    "Колобок повесился. Шерлок Холмс думает: Вот это поворот!",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я Вадик - твой помощник.\n\n"
        "Я умею:\n"
        "- Считать примеры (2+2)\n"
        "- Рассказывать анекдоты (/joke)\n"
        "- Показывать время (/time)\n"
        "- Погоду (/weather Москва)\n\n"
        "Просто напиши мне что-нибудь!"
    )

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(JOKES))

async def show_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now()
    await update.message.reply_text(f"Сейчас {now.strftime('%H:%M:%S')}\nСегодня {now.strftime('%d.%m.%Y')}")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши город: /weather Москва")
        return
    city = " ".join(context.args)
    await update.message.reply_text(f"Погода в {city}: +5°C, облачно")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if re.search(r'[\d\+\-\*/\(\)]', text):
        try:
            result = eval(text)
            await update.message.reply_text(f"Результат: {result}")
            return
        except:
            pass
    
    text_lower = text.lower()
    if "привет" in text_lower:
        answer = "Привет! Как дела?"
    elif "как дела" in text_lower:
        answer = "Отлично! А у тебя?"
    elif "кто ты" in text_lower:
        answer = "Я Вадик - твой помощник!"
    elif "пока" in text_lower:
        answer = "До встречи!"
    else:
        answer = f"Ты сказал: {text}"
    
    await update.message.reply_text(answer)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("time", show_time))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот Вадик запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
