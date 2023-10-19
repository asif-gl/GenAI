from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.register_user, name='signup'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('bot/', views.my_bot, name='bot'),
    path('generate_learning_path/', views.generate_learning_path, name='generate_learning_path')
]
