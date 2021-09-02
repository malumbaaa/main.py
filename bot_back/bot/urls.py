from django.urls import path
from .views import *
from rest_framework import routers


urlpatterns =[
    path('customer/', CustomerList.as_view()),
    path('customer/<int:pk>/', CustomerDetail.as_view()),
    path('product/', ProductList.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('product_photo/', ProductPhotoList.as_view()),
    path('product_photo/<int:pk>/', ProductPhotoDetail.as_view()),
    path('cart/', CartList.as_view()),
    path('cart/<int:pk>/', CartDetail.as_view()),
    path('cart_product/', CartProductList.as_view()),
    path('cart_product/<int:pk>/', CartProductDetail.as_view()),
    path('order/', OrderList.as_view()),
    path('order/<int:pk>/', OrderDetail.as_view()),

]