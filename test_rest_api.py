import unittest

from app import *
import json

class RestApiTestCase(unittest.TestCase):

    def setUp(self):
        """Initialize test variables and app"""
        self.client = app.test_client(self)
        self.app = app
        self.product_data = {
            'name': 'Shirt', 'size': 'XL', 'user_id': 1
        }
        self.product_data_update = {
            'name': 'Shirt Web', 'size': 'M', 'user_id': 1
        }

        req = self.client.post('/api/login', json = {
            "email": "admin@admin.com",
            "password": "secret"
        })
        res = req.get_json()
        self.token = res['access_token']
        with self.app.app_context():
            db.create_all()

    def test_01_create_product(self):
        req = self.client.post('/api/products',
                               json = self.product_data,
                               headers={"Authorization": "Bearer {}".format(self.token)})
        res = req.get_json()
        self.assertEqual(req.status_code, 200)
        self.assertEqual(res['message'], 'Successfully save data')

    def test_02_get_product(self):
        req = self.client.get(
            '/api/products/1',
            headers={"Authorization": "Bearer {}".format(self.token)})
        res = req.get_json()
        self.assertEqual(req.status_code, 200)
        self.assertEqual(res['message'], 'Successfully get data')

    def test_03_update_product(self):
        req = self.client.put('/api/products/1',
                              json = self.product_data_update,
                              headers={"Authorization": "Bearer {}".format(self.token)})
        res = req.get_json()
        self.assertEqual(req.status_code, 200)
        self.assertEqual(res['message'], 'Successfully update data')

    def test_04_delete_product(self):
        req = self.client.delete('/api/products/1',
                                 headers={"Authorization": "Bearer {}".format(self.token)})
        res = req.get_json()
        self.assertEqual(req.status_code, 200)
        self.assertEqual(res['message'], 'Successfully delete data')

    if __name__ == "__main__":
        unittest.main()
