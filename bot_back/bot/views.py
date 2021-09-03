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

    def put(self, request, *args, **kwargs):
        print(kwargs)
        print(request.data)
        print(type(Cart.objects.get(id=kwargs['pk'])))
        check = Cart.objects.get(id=kwargs['pk'])
        print(request.data['product_id'])
        return super(CartProductDetail, self).put(request, cart_id=check,
                                                            product_id=request.data['product_id'],
                                                  kwargs={'prikol': request.data})


class OrderList(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
            customer = Customer.objects.get(id=request.data['user_id'])
            # print(request.data['products'])
            # products = Product.objects.filter(id=request.data['products'][0]['id'])
            # print(products)
            money = 0
            for i in request.data['products']:
                 product = Product.objects.get(id=i)
                 money += int(product.price)
            # print(products, 'каго')
            # check = Product.objects.get(id=2)
            return super(OrderList, self).post(request, user_id=customer,
                                               status=request.data['status'],
                                               money=money,
                                               products=request.data['products'])


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer



# Create your views here.
