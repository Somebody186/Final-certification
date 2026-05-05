import unittest
import os
import json
from task_manager import TaskManager

class TestTaskManager(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "test_tasks.json"
        self.manager = TaskManager(self.test_file)
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_task(self):
        self.manager.add_task("Купить хлеб", "личное")
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0]["task"], "Купить хлеб")
        self.assertEqual(self.manager.tasks[0]["type"], "личное")
    
    def test_delete_task(self):
        self.manager.add_task("Пробежка", "здоровье")
        task_id = self.manager.tasks[0]["id"]
        self.manager.delete_task(task_id)
        self.assertEqual(len(self.manager.tasks), 0)
    
    def test_save_and_load(self):
        self.manager.add_task("Учёба", "учёба")
        new_manager = TaskManager(self.test_file)
        self.assertEqual(len(new_manager.tasks), 1)
        self.assertEqual(new_manager.tasks[0]["task"], "Учёба")
    
    def test_multiple_tasks(self):
        self.manager.add_task("Задача1", "работа")
        self.manager.add_task("Задача2", "личное")
        self.assertEqual(len(self.manager.tasks), 2)
        self.assertEqual(self.manager.tasks[0]["type"], "работа")
        self.assertEqual(self.manager.tasks[1]["type"], "личное")

if __name__ == "__main__":
    unittest.main()