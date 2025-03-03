import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd

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
    
    def generate_reports(self):
        """Генерация отчетов по посещаемости и популярным тренировкам в CSV."""
        conn = sqlite3.connect("fitness_club.db")
        df_visits = pd.read_sql_query("SELECT * FROM visits", conn)
        df_sessions = pd.read_sql_query("SELECT * FROM sessions", conn)
        conn.close()

        df_visits.to_csv("visits_report.csv", index=False)
        df_sessions.to_csv("sessions_report.csv", index=False)
        messagebox.showinfo("Успех", "Отчеты сохранены как CSV!")

    def add_client_window(self):
        """Окно для добавления клиента."""
        messagebox.showinfo("Функция", "Добавление клиента ещё не реализовано")

    def add_trainer_window(self):
        """Окно для добавления тренера."""
        messagebox.showinfo("Функция", "Добавление тренера ещё не реализовано")

    def add_session_window(self):
        """Окно для записи клиента на тренировку."""
        messagebox.showinfo("Функция", "Запись на тренировку ещё не реализована")

    def view_clients(self):
        """Просмотр всех клиентов."""
        messagebox.showinfo("Функция", "Просмотр клиентов ещё не реализован")

    def view_trainers(self):
        """Просмотр всех тренеров."""
        messagebox.showinfo("Функция", "Просмотр тренеров ещё не реализован")

    def add_visit_window(self):
        """Окно для фиксации посещения."""
        messagebox.showinfo("Функция", "Фиксация посещения ещё не реализована")
    
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
    root = tk.Tk()
    app = FitnessApp(root)
    root.mainloop()