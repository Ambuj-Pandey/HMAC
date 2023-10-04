from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken

# import models
from .models import User
from .models import FileModel

# import serializers
from .serializers import UserSerializer, FileSerializer

from django.contrib.auth import authenticate, login

@api_view(['POST'])
def upload_file(request):
    filename = request.data.get('selectedFile')
    description = request.data.get('desc')
    file = request.data.get('file')
    file_model = FileModel(filename=filename, description=description, file=file)
    file_model.save()

@api_view(['GET'])
def list_files_for_teacher(request):
    serializer = None 
    # if request.user.is_staff:   #isko baadmai karte
    files = FileModel.objects.all()
    # print(files)
    serializer = FileSerializer(files, many=True)
    print(files)
    return Response(serializer.data)  

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(request, email=email, password=password)
    print(user.is_staff)
    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Return tokens in the response
        response_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "is_staff": user.is_staff,  # Include the is_staff value
        }

        response = Response(response_data)
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    else:
        return Response({"error": "Login failed"}, status=400)
    

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

