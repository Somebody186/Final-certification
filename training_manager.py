import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.next_id = data.get("next_id", 1)
            except (json.JSONDecodeError, IOError):
                self.tasks = []
                self.next_id = 1
    
    def save_data(self):
        data = {
            "tasks": self.tasks,
            "next_id": self.next_id
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def add_task(self, task_text, task_type):
        task = {
            "id": self.next_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": task_type,
            "task": task_text
        }
        self.tasks.append(task)
        self.next_id += 1
        self.save_data()
    
    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save_data()