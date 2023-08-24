import unittest
from random import randint, choices
from unittest.mock import patch
from app1 import app
from task import AsyncResult, long_running_task , celery, my_task_instance

class TestMathUtils(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.app = app.test_client()

    def test_api_get(self):
        response = self.app.get('/account/decorator_class?a=5&b=80')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertListEqual(list(response.json.keys()), ['task_id', 'status'])
        task_id = response.json["task_id"]

        response = self.app.get(f'/account/get_result/{task_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertListEqual(list(response.json.keys()), ['task_id', 'status', 'get_result'])

    def test_api_post(self):
        response = self.app.post('/account/text')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertListEqual(list(response.json.keys()), ['task_id', 'status'])
        task_id = response.json["task_id"]
        
        response = self.app.get(f'/account/get_result/{task_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertListEqual(list(response.json.keys()), ['task_id', 'status', 'get_result'])


class TestMathUtils2(unittest.TestCase):
    def test_post(self):
        with patch("task.my_task_instance.update_state") as mock_func:
            mock_func.return_value = AsyncResult(
                'a4155a5d-8d0a-43e3-804b-bcb674b36f7a')
            response = my_task_instance.apply(args=[randint(1, 100), randint(1, 100)])
            self.assertEqual(mock_func.call_count, 1)

    def test_get(self):
        with patch("task.long_running_task.update_state") as mock_func:
            mock_func.return_value = AsyncResult(
                'a4155a5d-8d0a-43e3-804b-bcb674b36f7a')
            response = long_running_task.apply()
            self.assertEqual(mock_func.call_count, 100)

if __name__ == "__main__":
    unittest.main()