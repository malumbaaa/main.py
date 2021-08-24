from django.urls import path
from .views import *


urlpatterns =[
    path('customer/', CustomerList.as_view()),
    path('customer/<int:pk>/', CustomerDetail.as_view()),
    path('product/', ProductList.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('product_photo/', ProductPhotoList.as_view()),
    path('product_photo/<int:pk>/', ProductPhotoDetail.as_view()),
    path('cart/', CartList.as_view()),
    path('cart/<int:customer_id>/', CartDetail.as_view()),
    path('cart_product/', CartProductList.as_view()),
    path('cart_product/<int:cart_id>/', CartProductDetail.as_view()),
]