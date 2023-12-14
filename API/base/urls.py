from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.getRoutes, name='routes'),

    path('login/', views.login_view, name='login'),
    path('Upload/', views.upload_file, name='Upload'),

    path('teacher/files/', views.list_files_for_teacher, name='list_files_for_teacher'),
    path('aidetection/', views.AIContentDectection, name='AIContentDectection'),
    # path('logout/', views.LogoutView.as_view(), name ='logout')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)