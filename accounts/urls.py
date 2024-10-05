from django.urls import path
from .views import UserRegistrationView, UserLoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/', obtain_auth_token, name='api_token_auth'),
]
