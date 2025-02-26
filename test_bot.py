import telebot 
token='8037825172:AAGi30A88smYPAnCVP2SOIORnRhVgn1xA0k'
bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет ✌️ ")
print("Бот запущен...")
bot.infinity_polling()