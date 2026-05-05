import tkinter as tk
from tkinter import ttk, messagebox
from task_manager import TaskManager
import random

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("750x550")
        
        self.manager = TaskManager()
        
        # Предопределённый список задач для генерации
        self.predefined_tasks = [
            ("Написать отчёт", "работа"),
            ("Позвонить клиенту", "работа"),
            ("Сделать зарядку", "здоровье"),
            ("Купить продукты", "личное"),
            ("Прочитать главу книги", "учёба"),
            ("Помыть посуду", "личное"),
            ("Выучить 10 слов", "учёба"),
            ("Пробежка 3 км", "здоровье"),
            ("Составить план на неделю", "работа"),
            ("Проверить почту", "работа"),
        ]
        
        # === Панель добавления новой задачи ===
        add_frame = ttk.LabelFrame(root, text="Новая задача", padding=10)
        add_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(add_frame, text="Описание задачи:").grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = ttk.Entry(add_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Тип:").grid(row=0, column=2, padx=5, pady=5)
        self.type_var = tk.StringVar()
        types = ["работа", "личное", "здоровье", "учёба"]
        self.type_combo = ttk.Combobox(add_frame, textvariable=self.type_var, values=types, width=12)
        self.type_combo.grid(row=0, column=3, padx=5, pady=5)
        
        self.add_btn = ttk.Button(add_frame, text="Добавить задачу", command=self.add_custom_task)
        self.add_btn.grid(row=0, column=4, padx=5, pady=5)
        
        # === Генерация случайной задачи ===
        gen_frame = ttk.Frame(root)
        gen_frame.pack(fill="x", padx=10, pady=5)
        self.generate_btn = ttk.Button(gen_frame, text="🎲 Сгенерировать случайную задачу", command=self.generate_random_task)
        self.generate_btn.pack()
        
        # === Фильтрация ===
        filter_frame = ttk.LabelFrame(root, text="Фильтрация истории", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, padx=5)
        self.filter_type_var = tk.StringVar()
        self.filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, 
                                         values=["Все"] + types, width=12)
        self.filter_combo.set("Все")
        self.filter_combo.grid(row=0, column=1, padx=5)
        
        self.filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=0, column=2, padx=5)
        self.reset_btn = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        self.reset_btn.grid(row=0, column=3, padx=5)
        
        # === Таблица истории задач ===
        columns = ("id", "date", "type", "task")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("task", text="Задача")
        self.tree.column("id", width=40)
        self.tree.column("date", width=100)
        self.tree.column("type", width=100)
        self.tree.column("task", width=400)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0,10), pady=10)
        
        # === Удаление задачи ===
        del_frame = ttk.Frame(root)
        del_frame.pack(fill="x", pady=5)
        self.delete_btn = ttk.Button(del_frame, text="Удалить выбранную задачу", command=self.delete_selected)
        self.delete_btn.pack()
        
        self.refresh_table()
    
    def add_custom_task(self):
        task_text = self.task_entry.get().strip()
        task_type = self.type_var.get().strip()
        
        if not task_text:
            messagebox.showerror("Ошибка", "Введите описание задачи")
            return
        if task_type not in ["работа", "личное", "здоровье", "учёба"]:
            messagebox.showerror("Ошибка", "Выберите корректный тип задачи")
            return
        
        self.manager.add_task(task_text, task_type)
        self.refresh_table()
        self.task_entry.delete(0, tk.END)
        self.type_combo.set("")
    
    def generate_random_task(self):
        task_text, task_type = random.choice(self.predefined_tasks)
        self.manager.add_task(task_text, task_type)
        self.refresh_table()
        messagebox.showinfo("Сгенерировано", f"Добавлена задача: {task_text} [{task_type}]")
    
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for task in self.manager.tasks:
            self.tree.insert("", tk.END, values=(
                task["id"],
                task["date"],
                task["type"],
                task["task"]
            ))
    
    def apply_filter(self):
        filter_type = self.filter_type_var.get().strip()
        if filter_type == "Все" or not filter_type:
            filtered = self.manager.tasks
        else:
            filtered = [t for t in self.manager.tasks if t["type"] == filter_type]
        
        for row in self.tree.get_children():
            self.tree.delete(row)
        for task in filtered:
            self.tree.insert("", tk.END, values=(
                task["id"], task["date"], task["type"], task["task"]
            ))
    
    def reset_filter(self):
        self.filter_combo.set("Все")
        self.refresh_table()
    
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
            return
        task_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Подтверждение", "Удалить выбранную задачу из истории?"):
            self.manager.delete_task(task_id)
            self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()