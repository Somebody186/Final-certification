import json
import os
from datetime import datetime

class TrainingManager:
    def __init__(self, filename="trainings.json"):
        self.filename = filename
        self.trainings = []
        self.next_id = 1
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.trainings = data.

get("trainings", [])
                    self.next_id = data.get("next_id", 1)
            except (json.JSONDecodeError, IOError):
                self.trainings = []
                self.next_id = 1
    
    def save_data(self):
        data = {
            "trainings": self.trainings,
            "next_id": self.next_id
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def add_training(self, training):
        training["id"] = self.next_id
        self.trainings.append(training)
        self.next_id += 1
        self.save_data()
    
    def delete_training(self, training_id):
        self.trainings = [t for t in self.trainings if t["id"] != training_id]
        self.save_data()
    
    def filter_trainings(self, filter_date=None, filter_type=None):
        result = self.trainings.copy()
        
        if filter_date:
            result = [t for t in result if t["date"] == filter_date]
        
        if filter_type:
            result = [t for t in result if t["type"].lower() == filter_type.lower()]
        
        return result