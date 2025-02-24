from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomRegisterView, CustomLoginView, CustomLogoutView

app_name = 'user'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
]