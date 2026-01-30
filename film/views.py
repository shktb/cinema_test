from django.http import HttpResponse
from django.shortcuts import render
from film.models import Film

# Create your views here.

def index(request):
    return HttpResponse('heloo')

def film_list(request):
    film = Film.objects.all()
    return render(request, 'film_list.html', context={'list' : film}) 