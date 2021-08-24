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

    class Meta:
        fields = ['cart_id', 'product_id']
        model = CartProduct