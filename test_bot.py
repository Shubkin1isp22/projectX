from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, filters, CallbackQueryHandler


TOKEN = "8037825172:AAGi30A88smYPAnCVP2SOIORnRhVgn1xA0k"

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Мероприятия", callback_data='button_1'),
            InlineKeyboardButton("Регистрация", callback_data='button_2'),
            InlineKeyboardButton("Отзывы", callback_data='button_3'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я бот! Выбери кнопку:", reply_markup=reply_markup)

# Функция, которая обрабатывает нажатия кнопок
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Обязательно отвечаем на callback_query

    if query.data == 'button_1':
        await query.edit_message_text(text="Вы нажали Кнопка Мероприятия")
    elif query.data == 'button_2':
        await query.edit_message_text(text="Вы нажали Кнопка Регистрация")
    elif query.data == 'button_3':
        await query.edit_message_text(text="Вы нажали Кнопка Отзывы")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Обработчик нажатий на кнопки
    app.add_handler(CallbackQueryHandler(button))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()