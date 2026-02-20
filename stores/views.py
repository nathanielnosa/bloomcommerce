from rest_framework import status,serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from . models import Category,Products
from . serializers import CategorySerializer,ProductSerializer

from django.shortcuts import get_object_or_404

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
