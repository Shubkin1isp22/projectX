import telebot, threading, time
from telebot import types, TeleBot
from datetime import datetime, date, timedelta
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from database import get_events_from_db



load_dotenv()

DB_CONFIG = {
    "host": "localhost", 
    "port": "5432",  
    "user": "postgres",  
    "password": "Root1!?_",  
    "database": "tg_db"  
}

class BaseCommand(ABC):
    def __init__(self, bot : TeleBot):
        self.bot = bot

    @abstractmethod
    def command(self):
        pass

class InfoCommand(BaseCommand):
    def command(self):
        @self.bot.message_handler(commands=['info'])
        def info_command(message):
            #print("Команда info получена")
            chat_id = message.chat.id
            info_str = """
                            О нас

                            EventsBot — это ваш персональный помощник в мире событий. Мы создали этого бота, чтобы объединить всех, кто хочет быть в курсе интересных мероприятий, делиться своими и никогда не пропускать ничего важного.

                            С EventsBot вы можете:
                                •	📅 Просматривать актуальный список мероприятий
                                •	➕ Добавлять свои собственные события и делиться ими с другими
                                •	🔔 Получать своевременные напоминания, чтобы быть в нужном месте в нужное время

                            Наш бот создан с заботой о тех, кто ценит своё время и хочет быть частью активного сообщества. Неважно, организуете ли вы митап, лекцию, концерт или онлайн-встречу — EventsBot поможет вам найти свою аудиторию.

                            Мы верим, что события объединяют людей. А мы помогаем этим встречам происходить.

                            Присоединяйтесь — создавайте, узнавайте, приходите!
                            """
            self.bot.send_message(chat_id, info_str)




class Event:
    """Класс, представляющий мероприятие"""
    

    def __init__(self, E_id, name_event, time, userName, datetimee,):
        self.event_id=E_id
        self.event_name=name_event
        self.event_time = time
        self.event_datetime = self.event_datetime = datetime.strptime(datetimee, "%Y-%m-%d %H:%M:%S") if isinstance(datetimee, str) else datetimee
        self.event_organizer=userName
        self.available = self.Status()
        
    def create_event_datetime(self):
        """Создает объект datetime из event_date и event_time"""
        event_time_obj = self.event_datetime.date()  # Преобразуем строку времени в объект time
        return datetime.combine(self.event_date, event_time_obj)  # Объединяем date и time в datetime
        

    def Status(self):
        today = datetime.now()#Текущая дата и время 
        return self.event_datetime > today # Если Дата события не наступила, то оно доступно. Эта строка кидает False/True. Потом эту 
                                       # строку в аргумент берёт на 14 строке в статус(False/True)
        
    def __str__(self):
        """Вывод информации о мероприятии"""
        status= "Доступно" if self.available else "Закрыто"
        return f"{self.event_name} | {self.event_time} | {self.event_organizer} | {self.event_datetime} ({status}) \n"
    
    
    @staticmethod
    def get_total_events():
        """Получает количество мероприятий из базы данных"""
        from database import connect_db  # Импорт внутри метода
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events")
        result = cursor.fetchone()
        conn.close()
        return result[0]

class User:
    def __init__(self, message):
        self.tg_id = message.from_user.id
        self.tg_name = message.from_user.username 
        self.firstname = message.from_user.first_name
        
    def __str__(self):
        return f"Вы: {self.firstname}, Ваш tg_id: {self.tg_id}, Ваш username: {self.tg_name}"



class Notification:
    sent_notifications = set()  # Статическое поле для хранения отправленных уведомлений

    def __init__(self, event:'Event'):
        self.event = event

        
    def stat(self):
        now_time = datetime.now() # Текущая дата и время
        return now_time < self.event.event_datetime <= now_time + timedelta(minutes=60)
    
    def __str__(self):
        """Вывод Уведомления"""
        if self.stat():
            if self.event.event_name not in Notification.sent_notifications:
                Notification.sent_notifications.add(self.event.event_name)
                return f"Уведомление: {self.event.event_name} начнётся меньше чем через 1 час"
        return ""


class AddEvent:
    def __init__(self, bot, update_events_callback):
        self.bot = bot
        self.user_data = {} #Хранит временные данные для каждого пользователя
        self.update_events_callback = update_events_callback
        

    def setup_hadlers(self, message):
        chat_id = message.chat.id
        self.user_data[chat_id] = {}
        self.bot.send_message(chat_id, "Введите id мероприятия:")
        self.bot.register_next_step_handler(message, self.process_id)

    def process_id(self, message):
        chat_id = message.chat.id
        self.user_data[chat_id]['id'] = message.text
        self.bot.send_message(chat_id, "Введите название мероприятия:")
        self.bot.register_next_step_handler(message, self.process_name)

    def process_name(self, message):
        chat_id = message.chat.id
        self.user_data[chat_id]['name'] = message.text
        self.bot.send_message(chat_id, "Введите время начала (HH:MM:SS):")
        self.bot.register_next_step_handler(message, self.process_time)

    def process_time(self, message):
        chat_id = message.chat.id
        self.user_data[chat_id]['time'] = message.text
        self.bot.send_message(chat_id, "Введите дату и время мероприятия (ГГГГ-ММ-ДД) (HH:MM:SS):")
        self.bot.register_next_step_handler(message, self.process_date)

    def process_date(self, message):
        chat_id = message.chat.id
        self.user_data[chat_id]['datetime'] = message.text

        try:
            # Формируем данные и добавляем в БД
            user = message.from_user.username or "anon"
            from database import connect_db

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO events VALUES (%s, %s, %s, %s, %s)",
                (
                    self.user_data[chat_id]['id'],
                    self.user_data[chat_id]['name'],
                    self.user_data[chat_id]['time'],
                    user,
                    self.user_data[chat_id]['datetime']
                )
            )
            conn.commit()
            conn.close()

            self.bot.send_message(chat_id, "Мероприятие успешно создано!")
            self.update_events_callback()
        except ValueError:
            self.bot.send_message(chat_id, "Ошибка в формате даты или времени. Попробуйте снова.")

        self.user_data.pop(chat_id, None)




class EventBot:
    """Класс телеграм-бота для управления мероприятиями"""
    def __init__(self):
        self.token = '8037825172:AAGi30A88smYPAnCVP2SOIORnRhVgn1xA0k'
        self.bot = telebot.TeleBot(self.token) 
        self.events = get_events_from_db()
        self.setup_handlers()
        self.add_event_handler = AddEvent(self.bot, self.refresh_events)

    def setup_handlers(self):
        """Настройка команд и кнопок"""

        info_cmd = InfoCommand(self.bot) #подключение класса InfoCommandb
        info_cmd.command()



        @self.bot.message_handler(commands=['start', 'help'])
        def start_message(message):
            now = datetime.now().hour
            if 6 <= now < 12:
                day_period = "Доброе утро"
            elif 12 <= now < 23:
                day_period = "Добрый день"
            else:
                day_period = "Доброй ночи"
            self.bot.send_message(message.chat.id, day_period)

            # Запуск уведомлений в отдельном потоке
            threading.Thread(target=self.send_notifications, args=(message.chat.id,), daemon=True).start()

        @self.bot.message_handler(commands=['button'])
        def button_message(message):
            #print("Команда button получена")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Мероприятия")
            item2 = types.KeyboardButton("Профиль")
            item3 = types.KeyboardButton("Создать мероприятие")
            markup.add(item1, item2, item3)
            self.bot.send_message(message.chat.id, 'Выберите, что вам надо', reply_markup=markup)


        @self.bot.message_handler(commands=['all'])
        def all_message(message):
            #print("Команда all получена")
            total = Event.get_total_events()  # Вызов метода
            self.bot.send_message(message.chat.id, f"Всего мероприятий: {total}")


        @self.bot.message_handler(func=lambda message: True)
        def message_reply(message):
            if message.text == "Мероприятия":
                show_events = "\n".join(str(event) for event in self.events) if self.events else "Нет доступных мероприятий"

                self.bot.send_message(message.chat.id, show_events)
            elif message.text == "Профиль":
                usr_obj = User(message)
                show_user = str(usr_obj)
                self.bot.send_message(message.chat.id, show_user)

            elif message.text == "Создать мероприятие":
                self.add_event_handler.setup_hadlers(message)


    def send_notifications(self, chat_id):
        """Фоновая проверка уведомлений"""
        sent_notifications = set()
        while True:
            for event in self.events:
                notif_obj = Notification(event)
                notif_text = str(notif_obj)
                if notif_text and event.event_name not in sent_notifications:
                    self.bot.send_message(chat_id, notif_text)
                    sent_notifications.add(event.event_name)
            time.sleep(60)

    def refresh_events(self):
        """Обновление списка событий из базы данных"""
        self.events = get_events_from_db()

    def run(self):
        """Метод для запуска бота"""
        print("Бот запущен...")
        self.bot.infinity_polling()





if __name__ == "__main__":
    Tele = EventBot()
    Tele.run()