import mysql.connector



def connect_db():
    from test_bot import DB_CONFIG
    return mysql.connector.connect(**DB_CONFIG)

def get_events_from_db():
    from test_bot import Event
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events")  
    events = cursor.fetchall()
    conn.close()

    # Преобразуем строки из базы данных в объекты Event
    events_list = []
    for event in events:
        E_id, name_event, time, userName, datetimee = event
        events_list.append(Event(E_id, name_event, time, userName, datetimee))
    
    return events_list

