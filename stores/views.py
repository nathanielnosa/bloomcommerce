from django.urls import reverse
from rest_framework import status,serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from . models import *
from . serializers import *

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.conf import settings

import requests

# :::::: CRUD CATEGORY ::::::
# CREATE & RETRIEVE
class CategoryCreateRetrieveView(APIView):
    # post
    def post(self,request):
        try:
            serializers = CategorySerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # get all
    def get(self,request):
        try:
            categories = Category.objects.all()
            serializers = CategorySerializer(categories, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# RETRIEVE & UPDATE & DELETE
class CategoryRetrieveDeleteView(APIView):
    # get single
    def get(self,request,id):
        try:
            category = get_object_or_404(Category, id =id)
            serializers = CategorySerializer(category)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    # update
    def put(self,request,id):
        try:
            category = get_object_or_404(Category, id =id)
            serializers = CategorySerializer(category, data=request.data, partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
    # delete
    def delete(self,request,id):
        try:
            category = get_object_or_404(Category, id =id)
            category.delete()
            return Response({"Message":"Category Deleted"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# :::::: CRUD PRODUCT ::::::
# CREATE & RETRIEVE
class ProductCreateRetrieveView(APIView):
    # post
    def post(self,request):
        try:
            serializers = ProductSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # get all
    def get(self,request):
        try:
            products = Products.objects.all()
            serializers = ProductSerializer(products, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# RETRIEVE & UPDATE & DELETE
class ProductRetrieveDeleteView(APIView):
    # get single
    def get(self,request,id):
        try:
            product = get_object_or_404(Products, id =id)
            serializers = ProductSerializer(product)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    # update
    def put(self,request,id):
        try:
            product = get_object_or_404(Products, id =id)
            serializers = ProductSerializer(product, data=request.data, partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
    # delete
    def delete(self,request,id):
        try:
            product = get_object_or_404(Products, id =id)
            product.delete()
            return Response({"Message":"Product Deleted"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ADD PRODUCT TO CART
class AddProductToCart(APIView):
    def post(self,request,id):
        try:
            # get the product you want to add to cart
            product = get_object_or_404(Products,id=id)
            # create a session cart
            cart_id = request.session.get('cart_id',None)
            # price or discount
            price = product.discount_price if product.discount_price else product.price
            
            while transaction.atomic():
                if cart_id:
                    cart = Cart.objects.filter(id=cart_id).first()
                    if cart is None:
                        cart = Cart.objects.create(total=0)
                        request.session['cart_id'] = cart.id
                    
                    # if product in cart
                    this_product_in_cart = cart.cartproduct_set.filter(product=product)

                    if this_product_in_cart:
                        cartproduct = this_product_in_cart.last()
                        cartproduct.quantity +=1
                        cartproduct.subtotal +=price
                        cartproduct.save()
                        cart.total += price
                        cart.save()
                        return Response({"Message":"Item increase in cart"})
                    else:
                        cartproduct = CartProduct.objects.create(cart = cart,product = product,quantity =1,subtotal=price)
                        cartproduct.save()
                        cart.total +=price
                        cart.save()
                        return Response({"Message":"New product added to cart"})
                else:
                    cart = Cart.objects.create(total=0)
                    request.session['cart_id'] = cart.id
                    cartproduct = CartProduct.objects.create(cart = cart,product = product,quantity =1,subtotal=price)
                    cartproduct.save()
                    cart.total +=price
                    cart.save()
                    return Response({"Message":"A new cart created successfully"})
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# USERS CART
class MyCartView(APIView):
    def get(self,request):
        try:
            cart_id = request.session.get('cart_id',None)
            if cart_id:
                cart = get_object_or_404(Cart,id=cart_id)
                return Response({"Message":f"Profile - {cart.id}"})
            return Response({"Message":f"No profile found"})
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ManageCartView(APIView):
    def post(self,request,id):
        action =  request.data.get('action',None)
        try:
            cart_obj = CartProduct.objects.get(id=id)
            cart = cart_obj.cart
            price =cart_obj.product.discount_price if cart_obj.product.discount_price else cart_obj.product.price

            if action == "inc":
                cart_obj.quantity +=1
                cart_obj.subtotal +=price
                cart_obj.save()
                cart.total +=price
                cart.save()
                return Response({"Message":"Product increase in cart"})
            if action == "dcr":
                cart_obj.quantity -=1
                cart_obj.subtotal -=price
                cart_obj.save()
                cart.total -=price
                cart.save()
                if cart_obj.quantity ==0:
                    cart_obj.delete()
                return Response({"Message":"Product decrease in cart"})
            if action == "rmv":
                cart.total -=price
                cart.save()
                cart_obj.delete()
                return Response({"Message":"Product Removed in cart"})
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ::::: CHECKOUT VIEW ::::::
class CheckoutView(APIView):
    def post(self, request):
        try:
            cart_id = request.session.get('cart_id',None)
            if cart_id is None:
                return Response({"error":"You do not have an active cart"},status=status.HTTP_400_BAD_REQUEST)
            cart_obj = get_object_or_404(Cart, id=cart_id)

            serializers = CheckOutSerializer(data=request.data)
            if serializers.is_valid():
                order = serializers.save(
                    cart = cart_obj,
                    subtotal = cart_obj.total,
                    amount = cart_obj.total
                )
                del request.session['cart_id']
                
                if order.payment_method == "paystack":
                    payment_url = reverse('payment', args=[order.id])
                    return Response({"Redirect Payment Url": payment_url}, status=status.HTTP_200_OK)
                return Response({"Message":"Order created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# ::::: END OF CHECKOUT VIEW ::::::


# ::::: PAYMENT VIEW ::::::
class PaymentView(APIView):
    def get(self, request, id):
        try:
            order = get_object_or_404(Order, id=id)
            if order is None:
                return Response({"error":"Order not found"},status=status.HTTP_404_NOT_FOUND)
            
            url = "https://api.paystack.co/transaction/initialize" 
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            data = {
                "amount": order.amount * 100, 
                "email": order.email,
                "reference": order.ref,
            }
            response = requests.post(url, data=data, headers=headers)
            response_data = response.json()

            if response_data["status"]:
                paystack_url = response_data["data"]
                return Response(
                    {
                        'order':order.id,
                        'total':order.amount,
                        'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY,
                        'paystack_url':paystack_url

                    }, status=status.HTTP_200_OK
                )
            else:
                return Response({"error":"Payment initialization failed"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    def get(self,request,ref):
        try:
            order = get_object_or_404(Order, ref=ref)
            url = f'https://api.paystack.co/transaction/verify/{ref}'
            headers =headers = {
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            }
            response = requests.get(url,headers=headers)
            response_data = response.json()

            if response_data["status"] and response_data["data"]["status"] == "success":
                order.payment_completed = True
                order.order_status = "completed"
                order.save()
                return Response({"Message": "payment was successful"}, status= status.HTTP_200_OK)
            elif response_data["data"]["status"] == "abandoned":
                order.order_status = "pending"
                order.save()
                return Response({"Message": "payment was abandoned"}, status= status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Message":"Payment failed"}, status= status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"Message":"Invalid payment reference"}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			