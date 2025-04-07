import psycopg2

try:
    connection = psycopg2.connect(
        dbname="tg_db",
        user="postgres",
        password="Root1!?_",  # Укажите здесь пароль
        host="localhost",
        port="5432"
    )
    print("Подключение успешно")
except Exception as error:
    print(f"Ошибка: {error}")

def connect_db():
    from test_bot import DB_CONFIG
    return psycopg2.connect(**DB_CONFIG)

def get_events_from_db():
    from test_bot import Event
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")  
    events = cursor.fetchall()
    conn.close()

    # Преобразуем строки из базы данных в объекты Event
    events_list = []
    for event in events:
        e_id, name_event, time, username, datetimee = event
        events_list.append(Event(e_id, name_event, time, username, datetimee))
    
    return events_list

def add_event_to_db():
    from test_bot import EventBot, AddEvent
    conn = connect_db() # Создаёт коннект с бд, призывая func connect_db.
    cursor = conn.cursor() # Создаёт курсор, что бы работать с sql. Записывает его в переменную.

    cursor.execute("") # Через курсор идёт внедрение sql запроса

    conn.commit()
    conn.close() # Закрытие соединения с бд

