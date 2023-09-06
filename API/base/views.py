from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, logout

# import models
from .models import User

# import serializers
from .serializers import UserSerializer
# Create your views here.

class HomeView(APIView):
     
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}

        return Response(content)


# class LogoutView(APIView):
#      permission_classes = (IsAuthenticated,)
#      def post(self, request):
          
#           try:
#                refresh_token = request.data["refresh_token"]
#                token = RefreshToken(refresh_token)
#                token.blacklist()
#                return Response(status=status.HTTP_205_RESET_CONTENT)
#           except Exception as e:
#                return Response(status=status.HTTP_400_BAD_REQUEST)
          

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

