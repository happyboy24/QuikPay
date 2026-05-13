from django.urls import path
from .views import create_user, login

urlpatterns = [
    path('register/', create_user, name='register'),

    path("login/", login, name="login")
]