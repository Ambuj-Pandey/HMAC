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

import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
# import models
from .models import User
from .models import FileModel, FileComparisonModel

# import serializers
from .serializers import UserSerializer, FileSerializer


# my plan for AI content:

# uploads a file, trigger a signal, and in signal -> get the text ---and then AI would be calulate for that text


model_path = 'model'
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
num_labels = 2
model = DistilBertForSequenceClassification.from_pretrained(
    model_path, num_labels=num_labels)
model.eval()

@api_view(['POST'])
def upload_file(request):
    filename = request.data.get('selectedFile')
    description = request.data.get('desc')
    file = request.data.get('file')
    file_model = FileModel(
        filename=filename, description=description, file=file)
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
        max_similarity = FileComparisonModel.objects.filter(uploaded_file=file).aggregate(
            Max('similarity_result'))['similarity_result__max']

        similar_files = FileComparisonModel.objects.filter(
            uploaded_file=file, similarity_result=max_similarity)

        other_file_info[file.filename] = [f.other_file for f in similar_files]

        # Add the max_similarity to the dictionary with the file's name as the key
        # Default to 0.0 if no max_similarity found
        max_similarities[file.filename] = float(
            str(max_similarity*100)[:6]) if max_similarity is not None else 0.0

    serializer = FileSerializer(files, many=True)

    file_data = []
    for file in serializer.data:
        filename = file['filename']
        # Default to 0.0 if no max_similarity found
        max_similarity = max_similarities.get(filename, 0.0)
        uploader_info = file['uploaded_by']
        other_files = [FileSerializer(
            f).data for f in other_file_info.get(filename, None)]
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
        'file_data': file_data,
    }

    return Response(response_data)


@api_view(['POST', 'GET'])
def AIContentDectection(request):
    text = '''
            Google is an internet search engine. It uses a proprietary algorithm that’s designed to retrieve and order search results to provide the most relevant and dependable sources of data possible.

            Google’s stated mission is to “organize the world’s information and make it universally accessible and useful.” It is the top search engine in the world, a position that has generated criticism and concern about the power it has to influence the flow of online information.

            Google is so dominant that the term “Google” can also be used as a verb, so that when someone searches for something on Google, they may say they “Googled” it.
                '''
    inputs = tokenizer(text, return_tensors="pt")

    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        logits = outputs.logits

    probabilities = torch.softmax(logits, dim=1)

    percentage_probs = (probabilities * 100).tolist()[0]

    class_labels = [str(i) for i in range(num_labels)]

    class_percentage_dict = {label: percentage for label, percentage in zip(class_labels, percentage_probs)}

    for label, percentage in class_percentage_dict.items():
        print(f"Class {label}: {percentage:.2f}%")

    return Response(class_percentage_dict)


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
