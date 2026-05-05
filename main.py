import tkinter as tk
from tkinter import ttk, messagebox
from training_manager import TrainingManager

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("750x500")
        
        self.manager = TrainingManager()
        
        # Поля ввода
        input_frame = ttk.LabelFrame(root, text="Новая тренировка", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, padx=5, pady=5)
        self.type_var = tk.StringVar()
        types = ["Бег", "Велосипед", "Плавание", "Силовая", "Йога"]
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, values=types, width=12)
        self.type_combo.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, padx=5, pady=5)
        self.duration_entry = ttk.Entry(input_frame, width=10)
        self.duration_entry.grid(row=0, column=5, padx=5, pady=5)
        
        self.add_btn = ttk.Button(input_frame, text="Добавить тренировку", command=self.add_training)
        self.add_btn.grid(row=0, column=6, padx=10, pady=5)
        
        # Фильтры
        filter_frame = ttk.LabelFrame(root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0, padx=5)
        self.filter_date_entry = ttk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=2, padx=5)
        self.filter_type_var = tk.StringVar()
        self.filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, 
                                               values=["Все"] + types, width=12)
        self.filter_type_combo.set("Все")
        self.filter_type_combo.grid(row=0, column=3, padx=5)
        
        self.filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=0, column=4, padx=10)
        
        self.reset_btn = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        self.reset_btn.grid(row=0, column=5, padx=5)
        
        # Таблица для отображения
        columns = ("id", "date", "type", "duration")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("duration", text="Длительность (мин)")
        self.tree.column("id", width=40)
        self.tree.column("date", width=100)
        self.tree.column("type", width=120)
        self.tree.column("duration", width=100)
        
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure

scrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0,10), pady=10)
        
        # Кнопка удаления
        self.delete_btn = ttk.Button(root, text="Удалить выбранную", command=self.delete_selected)
        self.delete_btn.pack(pady=5)
        
        self.refresh_table()
    
    def add_training(self):
        date = self.date_entry.get().strip()
        training_type = self.type_var.get().strip()
        duration = self.duration_entry.get().strip()
        
        # Валидация
        if not date or not training_type or not duration:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        
        # Проверка формата даты
        try:
            from datetime import datetime
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return
        
        # Проверка длительности
        try:
            duration_min = float(duration)
            if duration_min <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
            return
        
        training = {
            "date": date,
            "type": training_type,
            "duration": duration_min
        }
        
        self.manager.add_training(training)
        self.refresh_table()
        
        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.type_combo.set("")
    
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for training in self.manager.trainings:
            self.tree.insert("", tk.END, values=(
                training["id"], 
                training["date"], 
                training["type"], 
                training["duration"]
            ))
    
    def apply_filter(self):
        filter_date = self.filter_date_entry.get().strip()
        filter_type = self.filter_type_var.get().strip()
        
        if filter_type == "Все":
            filter_type = None
        
        filtered = self.manager.filter_trainings(filter_date=filter_date if filter_date else None,
                                                  filter_type=filter_type)
        
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for training in filtered:
            self.tree.insert("", tk.END, values=(
                training["id"], 
                training["date"], 
                training["type"], 
                training["duration"]
            ))
    
    def reset_filter(self):
        self.filter_date_entry.delete(0, tk.END)
        self.filter_type_var.set("Все")
        self.refresh_table()
    
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите тренировку для удаления")
            return
        
        item = self.tree.item(selected[0])
        training_id = item["values"][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранную тренировку?"):
            self.manager.delete_training(training_id)
            self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()