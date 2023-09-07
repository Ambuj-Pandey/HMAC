from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('users/', views.getUsers, name='getUsers'),
    path('users/<str:id>/', views.getUser, name='getUser'),

    path('login/', views.login_view, name='login'),
    path('Upload/', views.upload_file, name='Upload'),
    # path('logout/', views.LogoutView.as_view(), name ='logout')
]