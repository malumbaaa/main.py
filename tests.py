import unittest
import requests

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    requests.get("http://127.0.0.1:8000/api/cart_products/")
    unittest.main()
