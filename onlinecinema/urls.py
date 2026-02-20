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
from film.views import (FilmListView, FilmCreateView, FilmDetailView, FilmDeleteView, BaseView, )

from django.conf.urls import static
from django.conf import settings
from users.views import RegisterView, LoginUserView, LogoutUserView, ProfileView, UpdateProfileView

class_film = [
    path('class/film', FilmListView.as_view(), name="film_list"),
    path("class/create", FilmCreateView.as_view(), name="film_create"),
    path("film/class/<int:film_id>/", FilmDetailView.as_view(), name="film_detail"),
    path("film/class/<int:film_id>/delete/", FilmDeleteView.as_view(), name="film_delete"),

]

films = [
    # path('film/', film_list),
    # path('film/<int:film_id>/', film_detail),
    # path("film_create/", film_create), 
    # path("film_delete/<int:film_id>/", film_delete),
]

users = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("update_profile/", UpdateProfileView.as_view(), name="update"),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BaseView.as_view(), name="base"),
    *users,
    *class_film,
] + static.static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
