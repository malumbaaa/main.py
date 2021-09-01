from rest_framework import generics
from .serializer import *
import requests


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductPhotoList(generics.ListCreateAPIView):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer


class ProductPhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer


class CartList(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartProductList(generics.ListCreateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer


class CartProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer


def Cart_view(request):
    print(request.content_params)
    cart = Cart.objects.get(id=request.GET['cart_id'])
    requests.put(f"http://127.0.0.1:8000/api/cart_product/request.GET['cart_id']/",
                 json={"product_id":request.GET['product_id'],
                       "id": cart},
                 headers={"Content-Type": "application/json"})




# Create your views here.
