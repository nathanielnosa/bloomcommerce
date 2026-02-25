import secrets
from rest_framework import serializers,status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

from . serializers import RegisterSerializer
from . models import Profile

# registration
class RegistrationView(APIView):
    def post(self,request):
        try:
            serializers = RegisterSerializer(data = request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# login
class LoginView(APIView):
    def post(self,request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return Response({"Message":f"{user.username} Login successful"}, status=status.HTTP_200_OK)
            return Response({"Message":"username/password not match"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"Error":str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# logout
class LogoutView(APIView):
    def post(self, request):
        try:
            logout(request)
            return Response({"Message":f"{request.user.username} logout successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Error":str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# dashboard
class DashboardView(APIView):
    def get(self,request):
        try:
            user_data = request.user
            return Response({"Message":f"Welcome {user_data}"})
        except Exception as e:
            return Response({"Error":str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
