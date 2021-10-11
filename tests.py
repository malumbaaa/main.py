from django.test import TestCase, Client
from .models import *


class TestCustomer(TestCase):
    def setUp(self) -> None:
        Customer.objects.create(name='Иван', surname='Иванов', username='@oskar')
        Customer.objects.create(name='Петр', surname='Сидоров', username='@laba')

    def test_models(self):
        user1 = Customer.objects.get(name='Иван')
        user2 = Customer.objects.get(name='Пётр')


class TestProduct(TestCase):
    def setUp(self) -> None:
        Product.objects.create(name='Майка', description='Лучшая майка', username='100$')
        Product.objects.create(name='Худи', surname='Лучшая худи', username='200$')

    def test_models(self):
        product1 = Product.objects.get(name='Майка')
        product2 = Product.objects.get(name='Худи')