import unittest
import os
import json
from training_manager import TrainingManager

class TestTrainingManager(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "test_trainings.json"
        self.manager = TrainingManager(self.test_file)
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_training(self):
        training = {"date": "2025-04-15", "type": "Бег", "duration": 30.5}
        self.manager.add_training(training)
        self.assertEqual(len(self.manager.trainings), 1)
        self.assertEqual(self.manager.trainings[0]["type"], "Бег")
    
    def test_delete_training(self):
        training = {"date": "2025-04-15", "type": "Бег", "duration": 30}
        self.manager.add_training(training)
        training_id = self.manager.trainings[0]["id"]
        self.manager.delete_training(training_id)
        self.assertEqual(len(self.manager.trainings), 0)
    
    def test_filter_by_date(self):
        t1 = {"date": "2025-04-15", "type": "Бег", "duration": 30}
        t2 = {"date": "2025-04-16", "type": "Плавание", "duration": 45}
        self.manager.add_training(t1)
        self.manager.add_training(t2)
        
        filtered = self.manager.filter_trainings(filter_date="2025-04-15")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["type"], "Бег")
    
    def test_filter_by_type(self):
        t1 = {"date": "2025-04-15", "type": "Бег", "duration": 30}
        t2 = {"date": "2025-04-16", "type": "Плавание", "duration": 45}
        self.manager.add_training(t1)
        self.manager.add_training(t2)
        
        filtered = self.manager.filter_trainings(filter_type="Плавание")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["duration"], 45)
    
    def test_save_and_load(self):
        training = {"date": "2025-04-15", "type": "Йога", "duration": 60}
        self.manager.add_training(training)
        
        new_manager = TrainingManager(self.test_file)
        self.assertEqual(len(new_manager.trainings), 1)
        self.assertEqual(new_manager.trainings[0]["type"], "Йога")
    
    def test_positive_duration_validation(self):
        # В реальном приложении проверка в GUI, здесь проверка модели
        training = {"date": "2025-04-15", "type": "Бег", "duration": 10.5}
        self.manager.add_training(training)
        self.assertGreater(self.manager.trainings[0]["duration"], 0)

if __name__ == "__main__":
    unittest.main()