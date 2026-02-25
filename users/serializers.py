from rest_framework import serializers
from django.contrib.auth.models import User

from . models import Profile
from . utils import emailSender

# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['username','email']
    
# profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSerializer()
        fields = ['fullname','gender','phone','profile_pix']

# registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    class Meta:
        model = Profile
        fields = ['fullname','username','email','password1','password2','gender','phone','profile_pix']

    def validate(self,data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password not match')
        return data
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password1')

        user = User.objects.create_user(username=username,email=email,password=password)

        profile = Profile.objects.create(
            user = user,
            fullname = validated_data['fullname'],
            gender = validated_data['gender'],
            phone = validated_data['phone'],
            profile_pix=validated_data['profile_pix']
        )
        emailSender(profile.fullname,email)
        return profile


