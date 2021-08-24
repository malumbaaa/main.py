from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", 'surname', 'username', 'date']


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", 'name', 'description', 'price']


class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', 'product_id']


class CartProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('product_id',)
    save_on_top = True
    list_display = ['cart_id',]


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPhoto, ProductPhotoAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct, CartProductAdmin)
