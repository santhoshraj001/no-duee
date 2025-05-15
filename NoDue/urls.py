"""NoDue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff_logout/', views.staff_logout, name='staff_logout'),
    path('student_details/', views.student_details, name='student_details'),
    path('all_stud/', views.all_stud, name='all_stud'),
    path('send_msg/<str:pk>/<str:amt>/', views.send_msg, name='send_msg'),
    path('all_due/', views.all_due, name='all_due'),
    path('insert_student/', views.insert_student, name='insert_student'),
    path('all_due/', views.all_due, name='all_due'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('', views.face_verification, name='face_verification'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)