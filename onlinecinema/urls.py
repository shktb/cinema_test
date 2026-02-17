"""
URL configuration for onlinecinema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from film.views import film_list, film_detail, base, film_create, film_delete
from django.conf.urls import static
from django.conf import settings
from users.views import register, login_user, logout_user, profile, update_profile
films = [
    path('film/', film_list),
    path('film/<int:film_id>/', film_detail),
    path("film_create/", film_create), 
    path("film_delete/<int:film_id>/", film_delete),
]

users = [
    path("register/", register),
    path("login/", login_user),
    path("profile/", profile),
    path("logout/", logout_user),
    path("update_profile/", update_profile),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base),
    *films,
    *users
] + static.static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
