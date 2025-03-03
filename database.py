import sqlite3

def init_db():
    conn = sqlite3.connect("fitness_club.db")
    cursor = conn.cursor()
    
    # Создание таблицы клиентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            phone TEXT,
            start_date TEXT,
            end_date TEXT,
            tariff TEXT
        )
    ''')
    
    # Создание таблицы тренеров
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trainers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT
        )
    ''')
    
    # Создание таблицы тренировок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            trainer_id INTEGER,
            session_type TEXT,
            session_time TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id),
            FOREIGN KEY(trainer_id) REFERENCES trainers(id)
        )
    ''')
    
    # Создание таблицы посещений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            visit_datetime TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("База данных и таблицы созданы.")
