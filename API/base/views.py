from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Max

# import models
from .models import User
from .models import FileModel, FileComparisonModel

# import serializers
from .serializers import UserSerializer, FileSerializer

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
    max_similarities = {}
    other_file_info = {}

    # Calculate the maximum similarity for each file
    for file in files:
        # Use an aggregation query to find the maximum similarity for this file
        max_similarity = FileComparisonModel.objects.filter(uploaded_file=file).aggregate(Max('similarity_result'))['similarity_result__max']

        similar_files = FileComparisonModel.objects.filter(uploaded_file=file, similarity_result=max_similarity)

        other_file_info[file.filename] = [f.other_file for f in similar_files]

        # Add the max_similarity to the dictionary with the file's name as the key
        max_similarities[file.filename] = max_similarity if max_similarity is not None else 0.0 # Default to 0.0 if no max_similarity found

    serializer = FileSerializer(files, many=True)

    file_data = []
    for file in serializer.data:
        filename = file['filename']
        max_similarity = max_similarities.get(filename, 0.0)  # Default to 0.0 if no max_similarity found
        uploader_info = file['uploaded_by']
        other_files = [FileSerializer(f).data for f in other_file_info.get(filename, None)]
        other_file_names = [f['filename'] for f in other_files]

        file_data.append({
            **file,
            'max_similarity': max_similarity,
            'uploaded_by_info': uploader_info,
            'other_files_with_max_similarity': other_files,
            'other_file_names': other_file_names
        })
        print(other_file_names)
        
    response_data = {
        'file_data':file_data,
    }

    return Response(response_data)  

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

