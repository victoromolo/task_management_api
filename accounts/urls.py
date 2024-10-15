from django.urls import path
from .views import UserRegistrationView, UserLoginView
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.contrib.auth.views import LogoutView

#urlpatterns = [
    #path('register/', UserRegistrationView.as_view(), name='register'),
    #path('login/', UserLoginView.as_view(), name='login'),
    #path('token/', obtain_auth_token, name='api_token_auth'),
#]

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('token/', obtain_auth_token, name='api_token_auth')
]