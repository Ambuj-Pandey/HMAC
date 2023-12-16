"""
URL configuration for API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': 'api/v1/',
            'method': 'GET',
            'body': None,
            'description': 'Returns available endpoints'
        },
        {
            'Endpoint': 'api/v1/login/',
            'method': 'POST',
            'body': {'username': 'your_username', 'password': 'your_password'},
            'description': 'User login'
        },
        {
            'Endpoint': 'api/v1/Upload/',
            'method': 'POST',
            'body': {'file': 'your_file'},
            'description': 'Upload a file'
        },
        {
            'Endpoint': 'api/v1/teacher/files/',
            'method': 'GET',
            'body': None,
            'description': 'List files for teacher'
        },
        # {
        #     'Endpoint': 'api/v1/aidetection/',
        #     'method': ['GET', 'POST'],
        #     'body': {
        #         'uploaded_by': "test@test.com",  
        #         'detection_results_Human': "38%",
        #         'detection_results_AI': "62%"
        #     },
        #     'description': 'AI Content Detection'
        # },
    ]

    return Response(routes)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', getRoutes, name='routes'),
    path("api/v1/", include("base.urls")),
    
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]


