from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'name', 'surname', 'username', 'date']
        model = Customer


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'name', 'description', 'price']
        model = Product


class ProductPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'url', 'product_id']
        model = ProductPhoto


class CartSerializer(serializers.ModelSerializer):

    def get_cart(self, customer_id):
        return Cart.objects.get(customer_id=customer_id)

    class Meta:
        fields = ['id', 'customer_id']
        model = Cart


class CartProductSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        product = 0
        for i in str(self.validated_data.get('product_id')):
            if i.isdigit():
                product = i
        try:
            cp = CartProduct.objects.get(cart_id=Cart.objects.get(id=self.data['cart_id']))
        except AttributeError:
            cart = Cart.objects.get(id=self.validated_data.get('cart_id'))
        if str(self).find('update') != -1:
            cp.product_id.add(product)
            cp.save()
        elif str(self).find('remove') != -1:
            cp.product_id.remove(product)
            cp.save()
        else:
            cp = CartProduct(cart_id=cart)
            cp.save()
            cp.product_id.add(product)
            cp.save()

    class Meta:
        fields = ['cart_id', 'product_id']
        model = CartProduct


class OrderSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        print(self)
        print(self.data)
        print(self.validated_data)

    class Meta:
        fields = ['user_id', 'products', 'money', 'date_come', 'date_out', 'status']
        model = Orders
