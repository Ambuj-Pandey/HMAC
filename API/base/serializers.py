from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from base.models import User
from django.contrib.auth import authenticate


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password',  'full_name']

    def create(self, clean_data):
        user = User.objects.create_user(
            clean_data['email'],
            clean_data['password'],
            full_name=clean_data['full_name'],
        )
        user.save()
        return user


class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, clean_data):
        user = authenticate(
            email=clean_data['Email'],
            password=clean_data['password']
        )
        if user is None:
            raise serializers.ValidationError("Invalid Credentials")
        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
