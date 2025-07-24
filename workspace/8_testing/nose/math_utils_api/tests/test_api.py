import unittest
from flask import Flask
from app.api import app

class TestApi(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_add_endpoint(self):
        response = self.client.post('/add', json={'a': 2, 'b': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 5)

    def test_subtract_endpoint(self):
        response = self.client.post('/subtract', json={'a': 5, 'b': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 2)

    def test_add_invalid_input(self):
        response = self.client.post('/add', json={'a': 'invalid', 'b': 3})
        self.assertEqual(response.status_code, 400)

    def test_multiply_endpoint(self):
        response = self.client.post('/multiply', json={'a': 2, 'b': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 6)

    def test_multiply_invalid_input(self):
        response = self.client.post('/multiply', json={'a': 'invalid', 'b': 3})
        self.assertEqual(response.status_code, 400)

    def test_divide_endpoint(self):
        response = self.client.post('/divide', json={'a': 6, 'b': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 2)

    def test_divide_invalid_input(self):
        response = self.client.post('/divide', json={'a': 'invalid', 'b': 3})
        self.assertEqual(response.status_code, 400)

    def test_divide_by_zero(self):
        response = self.client.post('/divide', json={'a': 6, 'b': 0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Cannot divide by zero')

    def test_health_check_endpoint(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')
        self.assertEqual(response.json['service'], 'math_utils_api')
        self.assertEqual(response.json['version'], '0.1.0')

    def test_root_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        print(response.json)
        self.assertEqual(response.json['status'], 'ok')

    def test_not_found_endpoint(self):
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Endpoint not found')
