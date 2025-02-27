import telebot
from telebot import types

token = '8037825172:AAGi30A88smYPAnCVP2SOIORnRhVgn1xA0k'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
	bot.send_message(message.chat.id,'Привет')
      
@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    
bot.infinity_polling()