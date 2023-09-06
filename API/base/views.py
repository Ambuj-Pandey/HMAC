from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

# import models
from django.contrib.auth.models import User

# import serializers
from .serializers import UserSerializer
# Create your views here.

# superuser credentials
# Username: a
# Password: a

def data(request):
    return HttpResponse("Hello World")

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/users/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of users'
        },
        {
            'Endpoint': '/users/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single user object'
        },
        {
            'Endpoint': '/users/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new user with data sent in post request'
        },
        {
            'Endpoint': '/users/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Updates an existing user with data sent in post request'
        },
        {
            'Endpoint': '/users/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes an exiting user'
        },
    ]

    return Response(routes)

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, id):
    users = User.objects.get(pk=id)
    serializer = UserSerializer(users, many=False)
    return Response(serializer.data)

