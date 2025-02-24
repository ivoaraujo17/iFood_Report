from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


# Create your views here.
class CustomRegisterView(CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('homepage')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('homepage')

