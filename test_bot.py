import telebot
from telebot import types
from datetime import datetime, date, timedelta


class Event:
    """Класс, представляющий мероприятие"""
    def __init__(self, event_id, event_name, event_time, event_date:str, event_organizer):
        self.event_id=event_id
        self.event_name=event_name
        self.event_time = event_time
        self.event_date = datetime.strptime(event_date, "%Y-%m-%d").date()  
        self.event_organizer=event_organizer
        self.available = self.Status()
         
    
    def create_event_datetime(self):
        """Создает объект datetime из event_date и event_time"""
        event_time_obj = datetime.strptime(self.event_time, "%H:%M").time() # Преобразуем строку времени в объект time
        return datetime.combine(self.event_date, event_time_obj)    # Объединяем date и time в datetime
    

    def Status(self):
        today = datetime.today() #Текущая дата и время  
        return self.create_event_datetime() > today # Если Дата события не наступила, то оно доступно. Эта строка кидает False/True. Потом эту строку
                                       # в аргумент берёт на 16 строке в статус(False/True)

    def __str__(self):
        """Вывод информации о мероприятии"""
        status= "Доступно" if self.available else "Закрыто"
        return f"{self.event_name} | {self.event_time} | {self.event_date} | {self.event_organizer} ({status})"
      

class User:
    def __init__(self, user_id, name, tg_name, password):
        self.user_id = user_id
        self.name = name
        self.tg_name = tg_name
        self.password = password
    
    def __str__(self):
        return f"Вы: {self.name}, Ваш tg: {self.tg_name}, Ваш пароль: {self.password}"



class Notification:
    def __init__(self, event:'Event'):
        self.event = event

        
    def stat(self):
        now_time = datetime.now() # Текущая дата и время
        return now_time < self.event.create_event_datetime() <= now_time + timedelta(minutes=60)
    
    def __str__(self):
        """Вывод Уведомления"""
        if self.stat():
            return f"Уведомление: {self.event.event_name} начнётся меньше чем через 1 час"
        return ""

class EventBot:
    """Класс телеграм-бота для управления мероприятиями"""
    def __init__(self):
        self.token = '8037825172:AAGi30A88smYPAnCVP2SOIORnRhVgn1xA0k'
        self.bot = telebot.TeleBot(self.token) 
        self.events = [
            Event(1001, 'Учебная практика', '21:50', '2025-02-27', 'N.N.B.'),
            Event(1002, 'Праздник 9 мая', '11:54', '2025-05-09', 'RF'),
            Event(1003, 'Праздник 24 февраля', '22:40', '2025-02-24', 'USSR'),
            Event(1004, 'Не Масленница', '21:30', '2025-02-27', 'Rus,'),
        ]
        
        @self.bot.message_handler(commands=['start', 'help'])
        def start_message(message):
            self.bot.send_message(message.chat.id,'Привет') 
            if self.events:
                i = 0
                for event in self.events:
                    
                    eventik = self.events[i]      
                    self.notif_obj = Notification(eventik)
                    notif_text = str(self.notif_obj)  # Получаем текст уведомления
                    if notif_text:  # Отправляем, только если строка не пустая
                        self.bot.send_message(message.chat.id, notif_text)
                    i+=1
            else:
                self.bot.send_message(message.chat.id, 'Нет доступных событий')        

        @self.bot.message_handler(commands=['button'])
        def button_message(message):
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Мероприятия")
            item2=types.KeyboardButton("Войти/Зарегистрироваться")
            item3=types.KeyboardButton("Отзывы")
            markup.add(item1, item2, item3)
            self.bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

        @self.bot.message_handler(content_types='text')
        def message_reply(message):
            if message.text == "Мероприятия":
                show_events = "\n".join(str(event)for event in self.events) if self.events else "Нет доступных мероприятий"
                self.bot.send_message(message.chat.id, show_events)
            elif message.text == "Войти/Зарегистрироваться":
                markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                item4=types.KeyboardButton("Войти")
                item5=types.KeyboardButton("Зарегистрироваться")
                item6=types.KeyboardButton("Назад")
                markup.add(item4, item5, item6)
                self.bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
            elif message.text == "Назад":
                markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1=types.KeyboardButton("Мероприятия")
                item2=types.KeyboardButton("Войти/Зарегистрироваться")
                item3=types.KeyboardButton("Отзывы")
                markup.add(item1, item2, item3)
                self.bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
            elif message.text == "Отзывы":
                self.bot.send_message(message.chat.id, 'Здесь будут отзывы')
            
    def run(self):
        """Метод для запуска бота"""
        print("Бот запущен...")
        self.bot.infinity_polling()




    
if __name__ == "__main__":
    Tele = EventBot()
    Tele.run()