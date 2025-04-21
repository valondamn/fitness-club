import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
from database import init_db  # Импортируем функцию инициализации БД
import numpy as np

class FitnessApp:
    """Графический интерфейс для системы фитнес-клуба."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления фитнес-клубом")
        self.root.geometry("500x500")

        # Кнопки для действий
        tk.Button(root, text="Добавить клиента", command=self.add_client_window).pack(pady=5)
        tk.Button(root, text="Добавить тренера", command=self.add_trainer_window).pack(pady=5)
        tk.Button(root, text="Записать на тренировку", command=self.add_session_window).pack(pady=5)
        tk.Button(root, text="Просмотреть всех клиентов", command=self.view_clients).pack(pady=5)
        tk.Button(root, text="Просмотреть всех тренеров", command=self.view_trainers).pack(pady=5)
        tk.Button(root, text="Зафиксировать посещение", command=self.add_visit_window).pack(pady=5)
        tk.Button(root, text="Поиск клиентов", command=self.search_clients_window).pack(pady=5)
        tk.Button(root, text="Генерировать отчеты", command=self.generate_reports).pack(pady=5)
        tk.Button(root, text="Показать статистику", command=self.show_statistics).pack(pady=5)

    
    def generate_reports(self):
        """Генерация отчетов по посещаемости и популярным тренировкам в CSV."""
        conn = sqlite3.connect("fitness_club.db")
        df_visits = pd.read_sql_query("SELECT * FROM visits", conn)
        df_sessions = pd.read_sql_query("SELECT * FROM sessions", conn)
        conn.close()

        df_visits.to_csv("visits_report.csv", index=False)
        df_sessions.to_csv("sessions_report.csv", index=False)
        messagebox.showinfo("Успех", "Отчеты сохранены как CSV!")

    def show_statistics(self):
        """Вывод статистики по посещаемости, популярным тренерам и возрасту клиентов."""
        conn = sqlite3.connect("fitness_club.db")
        df_visits = pd.read_sql_query("SELECT * FROM visits", conn)
        df_sessions = pd.read_sql_query("SELECT trainer_id FROM sessions", conn)
        df_clients = pd.read_sql_query("SELECT age FROM clients", conn)
        conn.close()

        avg_visits = np.mean(df_visits["client_id"].value_counts()) if not df_visits.empty else 0
        top_trainers = df_sessions["trainer_id"].value_counts().head(3).to_dict()
        avg_age = np.mean(df_clients["age"]) if not df_clients.empty else 0

        stats_message = (
            f"Средняя посещаемость: {avg_visits:.2f}\n"
            f"Топ-3 популярных тренеров: {top_trainers}\n"
            f"Средний возраст клиентов: {avg_age:.2f}"
        )

        messagebox.showinfo("Статистика клуба", stats_message)

    def add_client_window(self):
        """Окно для добавления клиента."""
        # Здесь можно создать окно с формой для ввода данных клиента
        win = tk.Toplevel(self.root)
        win.title("Добавить клиента")
        win.geometry("400x300")
        
        tk.Label(win, text="Имя:").pack()
        name_entry = tk.Entry(win)
        name_entry.pack()

        tk.Label(win, text="Возраст:").pack()
        age_entry = tk.Entry(win)
        age_entry.pack()

        tk.Label(win, text="Телефон:").pack()
        phone_entry = tk.Entry(win)
        phone_entry.pack()

        tk.Label(win, text="Дата начала абонемента (YYYY-MM-DD):").pack()
        start_date_entry = tk.Entry(win)
        start_date_entry.pack()

        tk.Label(win, text="Дата окончания абонемента (YYYY-MM-DD):").pack()
        end_date_entry = tk.Entry(win)
        end_date_entry.pack()

        tk.Label(win, text="Тариф:").pack()
        tariff_entry = tk.Entry(win)
        tariff_entry.pack()

        def save_client():
            name = name_entry.get()
            age = age_entry.get()
            phone = phone_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            tariff = tariff_entry.get()
            
            conn = sqlite3.connect("fitness_club.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clients (name, age, phone, start_date, end_date, tariff) VALUES (?, ?, ?, ?, ?, ?)",
                           (name, age, phone, start_date, end_date, tariff))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Клиент успешно добавлен!")
            win.destroy()

        tk.Button(win, text="Сохранить", command=save_client).pack(pady=10)

    def add_trainer_window(self):
        """Окно для добавления тренера."""
        win = tk.Toplevel(self.root)
        win.title("Добавить тренера")
        win.geometry("400x200")
        
        tk.Label(win, text="Имя тренера:").pack()
        name_entry = tk.Entry(win)
        name_entry.pack()

        tk.Label(win, text="Специализация:").pack()
        specialization_entry = tk.Entry(win)
        specialization_entry.pack()

        def save_trainer():
            name = name_entry.get()
            specialization = specialization_entry.get()
            conn = sqlite3.connect("fitness_club.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO trainers (name, specialization) VALUES (?, ?)", (name, specialization))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Тренер успешно добавлен!")
            win.destroy()

        tk.Button(win, text="Сохранить", command=save_trainer).pack(pady=10)

    def add_session_window(self):
        """Окно для записи клиента на тренировку."""
        win = tk.Toplevel(self.root)
        win.title("Записать на тренировку")
        win.geometry("400x400")
        
        tk.Label(win, text="ID клиента:").pack()
        client_id_entry = tk.Entry(win)
        client_id_entry.pack()

        tk.Label(win, text="ID тренера:").pack()
        trainer_id_entry = tk.Entry(win)
        trainer_id_entry.pack()

        tk.Label(win, text="Тип тренировки (групповая/персональная):").pack()
        session_type_entry = tk.Entry(win)
        session_type_entry.pack()

        tk.Label(win, text="Время тренировки (YYYY-MM-DD HH:MM):").pack()
        session_time_entry = tk.Entry(win)
        session_time_entry.pack()

        def save_session():
            client_id = client_id_entry.get()
            trainer_id = trainer_id_entry.get()
            session_type = session_type_entry.get()
            session_time = session_time_entry.get()
            conn = sqlite3.connect("fitness_club.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sessions (client_id, trainer_id, session_type, session_time) VALUES (?, ?, ?, ?)",
                           (client_id, trainer_id, session_type, session_time))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Запись на тренировку сохранена!")
            win.destroy()

        tk.Button(win, text="Сохранить", command=save_session).pack(pady=10)

    def view_clients(self):
        """Просмотр всех клиентов."""
        conn = sqlite3.connect("fitness_club.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
        conn.close()
        
        win = tk.Toplevel(self.root)
        win.title("Список клиентов")
        win.geometry("500x400")
        
        text = tk.Text(win)
        text.pack(fill=tk.BOTH, expand=True)
        for client in clients:
            text.insert(tk.END, f"{client}\n")

    def view_trainers(self):
        """Просмотр всех тренеров."""
        conn = sqlite3.connect("fitness_club.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trainers")
        trainers = cursor.fetchall()
        conn.close()
        
        win = tk.Toplevel(self.root)
        win.title("Список тренеров")
        win.geometry("500x400")
        
        text = tk.Text(win)
        text.pack(fill=tk.BOTH, expand=True)
        for trainer in trainers:
            text.insert(tk.END, f"{trainer}\n")

    def add_visit_window(self):
        """Окно для фиксации посещения."""
        win = tk.Toplevel(self.root)
        win.title("Зафиксировать посещение")
        win.geometry("400x200")
        
        tk.Label(win, text="ID клиента:").pack()
        client_id_entry = tk.Entry(win)
        client_id_entry.pack()

        def save_visit():
            client_id = client_id_entry.get()
            from datetime import datetime
            visit_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect("fitness_club.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO visits (client_id, visit_datetime) VALUES (?, ?)", (client_id, visit_datetime))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Посещение зафиксировано!")
            win.destroy()

        tk.Button(win, text="Зафиксировать", command=save_visit).pack(pady=10)

    def search_clients_window(self):
        """Окно поиска клиентов по ФИО или фильтрации активных абонементов."""
        win = tk.Toplevel(self.root)
        win.title("Поиск клиентов")
        win.geometry("400x300")

        tk.Label(win, text="Введите ФИО клиента:").pack()
        search_entry = tk.Entry(win)
        search_entry.pack()

        def search_by_name():
            """Ищет клиента по ФИО."""
            name = search_entry.get()
            conn = sqlite3.connect("fitness_club.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE name LIKE ?", ('%' + name + '%',))
            clients = cursor.fetchall()
            conn.close()

            result_text.delete("1.0", tk.END)
            if clients:
                for client in clients:
                    result_text.insert(tk.END, f"{client}\n")
            else:
                result_text.insert(tk.END, "Клиенты не найдены.")

        def filter_active_subscriptions():
            """Фильтрует клиентов с активными абонементами."""
            conn = sqlite3.connect("fitness_club.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE end_date >= date('now')")
            clients = cursor.fetchall()
            conn.close()

            result_text.delete("1.0", tk.END)
            if clients:
                for client in clients:
                    result_text.insert(tk.END, f"{client}\n")
            else:
                result_text.insert(tk.END, "Нет активных абонементов.")

        tk.Button(win, text="Искать по ФИО", command=search_by_name).pack(pady=5)
        tk.Button(win, text="Фильтр: Активные абонементы", command=filter_active_subscriptions).pack(pady=5)

        result_text = tk.Text(win, height=10, width=50)
        result_text.pack()

if __name__ == "__main__":
    # Инициализация базы данных (выполнить один раз)
    from database import init_db
    init_db()

    root = tk.Tk()
    app = FitnessApp(root)
    root.mainloop()
