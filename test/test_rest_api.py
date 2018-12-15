import unittest

from app import *
import json

class RestApiTestCase(unittest.TestCase):

    def setUp(self):
        """Initialize test variables and app"""
        self.client = app.test_client(self)
        self.product_data = {
            'name': 'Shirt', 'size': 'XL', 'user_id': 1
        }
        self.product_data_update = {
            'name': 'Shirt Web', 'size': 'M', 'user_id': 1
        }
        with self.app.app_context():
            db.create_all()
            user = User('rifkyaziz@yandex.com', 'secret')
            db.session.add(user)
            db.session.commit()

    def test_create_product(self):
        req = self.client.post('/api/products/', json = self.product_data)
        res = req.get_json()
        res_data = res.data
        self.assertEqual(res.response_code, 200)
        self.assertEqual(res_data['message'], 'Successfully save data')
        self.assertEqual(res_data['data'], req_data)

    def test_get_product(self):
        req = self.client.get('/api/products/1')
        res = req.get_json()
        res_data = res.data
        self.assertEqual(res.response_code, 200)
        self.assertEqual(res_data['message'], 'Successfully get data')
        self.assertEqual(res_data['data'], self.product_data)

    def test_update_product(self):
        req = self.client.put('/api/products/1', json = self.product_data_update)
        res = req.get_json()
        res_data = res.data
        self.assertEqual(res.response_code, 200)
        self.assertEqual(res_data['message'], 'Successfully delete data')
        self.assertEqual(res_data['data'], self.product_data_update)

    def test_delete_product(self):
        req = self.client.delete('/api/products/1')p
        res = req.get_json()
        res_data = res.data
        self.assertEqual(res.response_code, 200)
        self.assertEqual(res_data['message'], 'Successfully delete data')
