from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForms, LoginForms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.

# Аунтентификация - поиск пользователя в бд
# Авторизация - проверка прав доступа пользователя 
# Регистрация - создание нового пользователя


def register(request):
    if request.method == "GET":
        forms = RegisterForms()
        return render(request, "users/register.html", context={"forms": forms})
    if request.method == "POST":
        forms = RegisterForms(request.POST)
        if not forms.is_valid():
            print(forms.errors)
            return HttpResponse("Error")
        User.objects.create_user(
            username=forms.cleaned_data.get("username"), 
            password=forms.cleaned_data.get("password"),
        )
    return redirect("/")

def login_user(request):
    if request.method == "GET":
        forms = LoginForms()
        return render(request, "users/login.html", context={"forms": forms})
    if request.method == "POST":
        forms = LoginForms(request.POST)
        if not forms.is_valid():
            return HttpResponse('Error')
        user = authenticate(
            request,
            username=forms.cleaned_data.get("username"),
            password=forms.cleaned_data.get("password"),
        )
        login(request, user)
    
    return redirect("/")

def logout_user(request):
    logout(request)
    return redirect("/")