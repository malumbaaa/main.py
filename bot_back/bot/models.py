from django.db import models
from django.utils import timezone

class Customer(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField(max_length=10)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductPhoto(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.TextField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product_id')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Product Photo'
        verbose_name_plural = 'Product Photos'


class Cart(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='customer_id')

    def __str__(self):
        return str(id)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartProduct(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='cart_id', primary_key=True, auto_created=True)
    product_id = models.ManyToManyField(Product, verbose_name='Products', blank=True)

    def __str__(self):
        return str(self.cart_id)

    class Meta:
        verbose_name = 'CartProduct'
        verbose_name_plural = 'CartProducts'


stats = [
    ('Поступил', 'Поступил'),
    ('Отправлен', 'Отправлен'),
    ('Ожидает', 'Ожидает'),
    ("Оплачен", "Оплачен")
]


class Orders(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='customer_id')
    status = models.TextField(stats)
    money = models.TextField(blank=True)
    date_come = models.DateTimeField(auto_created=True, blank=True)
    date_out = models.DateTimeField(blank=True, default=timezone.now())
    delivery = models.CharField(max_length=40, default="Самовывоз")
    products = models.ManyToManyField(Product, verbose_name='order_products')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
