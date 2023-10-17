from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.register_user, name='signup'),
    path('bot/', views.final_result, name='bot')
    # path('documenst/', views.)
]
