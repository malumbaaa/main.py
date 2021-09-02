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

    class Meta:
        fields = ['id', 'customer_id']
        model = Cart


class CartProductSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        product = 0
        print(self)
        print(str(self).find('update'))
        for i in str(self.validated_data.get('product_id')):
            if i.isdigit():
                product = i
        cp = CartProduct.objects.get(cart_id=Cart.objects.get(id=self.data['cart_id']))
        if str(self).find('update') != -1:
            cp.product_id.add(product)
            print(cp.product_id)
            cp.save()
        elif str(self).find('remove') != -1:
            cp.product_id.remove(product)
            print(cp.product_id)
            cp.save()

    class Meta:
        fields = ['cart_id', 'product_id']
        model = CartProduct


class OrderSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        print(self)
        print(self.data)
        print(kwargs)

    class Meta:
        fields = ['user_id', 'products', 'money', 'date_come', 'date_out', 'status']
        model = Orders
