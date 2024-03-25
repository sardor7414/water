from django.urls import path
from .views import UserLoginAPI, UserRegisterAPI, LogoutAPIView


urlpatterns = [
    path('login/', UserLoginAPI.as_view()),
    path('register/', UserRegisterAPI.as_view()),
    path('logout/', LogoutAPIView.as_view())
]
