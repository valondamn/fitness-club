import sqlite3

class Client:
    """Класс для работы с клиентами фитнес-клуба."""
    def __init__(self, name, age, phone, start_date, end_date, plan):
        self.name = name
        self.age = age
        self.phone = phone
        self.start_date = start_date
        self.end_date = end_date
        self.plan = plan

    def save_to_db(self):
        """Сохранение клиента в базу данных."""
        conn = sqlite3.connect("fitness_club.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO clients (name, age, phone, start_date, end_date, plan)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (self.name, self.age, self.phone, self.start_date, self.end_date, self.plan))
        conn.commit()
        conn.close()

class Trainer:
    """Класс для работы с тренерами."""
    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        """Сохранение тренера в базу данных."""
        conn = sqlite3.connect("fitness_club.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO trainers (name)
        VALUES (?)
        """, (self.name,))
        conn.commit()
        conn.close()

class Session:
    """Класс для записи клиентов на тренировки."""
    def __init__(self, client_id, trainer_id, session_type, session_time):
        self.client_id = client_id
        self.trainer_id = trainer_id
        self.session_type = session_type  # Групповая или персональная
        self.session_time = session_time

    def save_to_db(self):
        """Сохранение тренировки в базу данных."""
        conn = sqlite3.connect("fitness_club.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO sessions (client_id, trainer_id, session_type, session_time)
        VALUES (?, ?, ?, ?)
        """, (self.client_id, self.trainer_id, self.session_type, self.session_time))
        conn.commit()
        conn.close()

class Visit:
    """Класс для учёта посещений."""
    def __init__(self, client_id, visit_time):
        self.client_id = client_id
        self.visit_time = visit_time

    def save_to_db(self):
        """Сохранение посещения в базу данных."""
        conn = sqlite3.connect("fitness_club.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO visits (client_id, visit_time)
        VALUES (?, ?)
        """, (self.client_id, self.visit_time))
        conn.commit()
        conn.close()

def view_all_data():
    """Просмотр всех данных в базе данных."""
    conn = sqlite3.connect("fitness_club.db")
    cursor = conn.cursor()
    
    print("\nКлиенты:")
    for row in cursor.execute("SELECT * FROM clients"):
        print(row)
    
    print("\nТренеры:")
    for row in cursor.execute("SELECT * FROM trainers"):
        print(row)
    
    conn.close()

def view_all_sessions():
    """Просмотр всех записанных тренировок."""
    conn = sqlite3.connect("fitness_club.db")
    cursor = conn.cursor()
    print("\nТренировки:")
    for row in cursor.execute("SELECT * FROM sessions"):
        print(row)
    conn.close()

if __name__ == "__main__":
    # Тестируем добавление клиента
    client = Client("Иван Иванов", 30, "+79111234567", "2024-03-01", "2024-09-01", "Полный доступ")
    client.save_to_db()
    print("Клиент добавлен в базу данных.")
    
    # Тестируем добавление тренера
    trainer = Trainer("Алексей Смирнов")
    trainer.save_to_db()
    print("Тренер добавлен в базу данных.")
    
    # Тестируем запись на тренировку
    session = Session(1, 1, "Персональная", "2024-03-10 18:00")
    session.save_to_db()
    print("Клиент записан на тренировку.")
    
    # Тестируем фиксацию посещения
    visit = Visit(1, "2024-03-02 10:00")
    visit.save_to_db()
    print("Посещение зафиксировано.")
    
    # Просмотр всех данных
    view_all_data()
    
    # Просмотр всех тренировок
    view_all_sessions()
