from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForms, LoginForms, UpdateProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView, UpdateView, View
# Create your views here.

# Аунтентификация - поиск пользователя в бд
# Авторизация - проверка прав доступа пользователя 
# Регистрация - создание нового пользователя

class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForms
    success_url = reverse_lazy("base")  

    def form_valid(self, form):
        User.objects.create_user(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password"),
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

# def register(request):
#     if request.method == "GET":
#         forms = RegisterForms()
#         return render(request, "users/register.html", context={"forms": forms})
#     if request.method == "POST":
#         forms = RegisterForms(request.POST)
#         if not forms.is_valid():
#             print(forms.errors)
#             return HttpResponse("Error")
#         User.objects.create_user(
#             username=forms.cleaned_data.get("username"), 
#             password=forms.cleaned_data.get("password"),
#         )
#     return redirect("/")

class LoginUserView(FormView):
    template_name = "users/login.html"
    form_class = LoginForms
    success_url = reverse_lazy("base")

    def form_valid(self, form):
        user = authenticate(
            self.request,
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password"),
        )
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Неверный логин или пароль")
            return self.form_invalid(form)
        
# def login_user(request):
#     if request.method == "GET":
#         forms = LoginForms()
#         return render(request, "users/login.html", context={"forms": forms})
#     if request.method == "POST":
#         forms = LoginForms(request.POST)
#         if not forms.is_valid():
#             return HttpResponse('Error')
#         user = authenticate(
#             request,
#             username=forms.cleaned_data.get("username"),
#             password=forms.cleaned_data.get("password"),
#         )
#         login(request, user)
    
#     return redirect("/")

class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect("/")

# def logout_user(request):
#     logout(request)
#     return redirect("/")

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        initial_data = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'age': request.user.profile.age,
        }
        form = UpdateProfileForm(initial=initial_data)
        return render(request, "users/update_profile.html", {"form": form})

    def post(self, request):
        form = UpdateProfileForm(request.POST, request.FILES) # Обязательно request.FILES
        if form.is_valid():
            user = request.user
            profile = user.profile
            
            # Обновляем профиль (только если картинка передана)
            profile.age = form.cleaned_data.get("age")
            new_image = form.cleaned_data.get("image")
            if new_image:
                profile.image = new_image
            
            # Обновляем данные пользователя
            user.username = form.cleaned_data.get("username")
            user.email = form.cleaned_data.get("email")
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            
            user.save()
            profile.save()
            return redirect("film_list")
        
# def profile(request):
#     return render(request, "users/profile.html")

# def update_profile(request):
#     if request.method == "GET":
#         forms = UpdateProfileForm(request.POST or None)
#         return render(request, "users/update_profile.html", context={"forms": forms})

#     if request.method == "POST":
#         forms = UpdateProfileForm(request.POST, request.FILES)
#         if not forms.is_valid():
#             return HttpResponse("Error")
#         request.user.profile.age = forms.cleaned_data.get("age")
#         request.user.profile.image = forms.cleaned_data.get("image")

#         request.user.username = forms.cleaned_data.get("username")
#         request.user.email = forms.cleaned_data.get("email")
#         request.user.first_name = forms.cleaned_data.get("first_name")
#         request.user.last_name = forms.cleaned_data.get("last_name")

#         request.user.save()
#         request.user.profile.save()

#         return redirect("/film/")