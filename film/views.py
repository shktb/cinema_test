from django.http import HttpResponse
from django.shortcuts import render
from film.models import Film


# select * from product;
# Product.objects.all()


# select * from product where id= '2';
# Product.objects.get(id=2)  == возвращает 1 обьект

# select * from product where name = 'laptop';
# Product.objects.filter(name='laptop')

# select * from product $LIKE where name = 'laptop' and price = '1000';
# Product.objects.filter(name__icontains='laptop', price=1000)

# Product.objects.create(name='laptop', price=1000, description='laptop')

# Product.objects.update(price=1000) - изменение всех продуктов

# Product.objects.delete()


# Create your views here.

def film_list(request):
    films = Film.objects.all()
    return render(request, 'films_templates/film_list.html', context={'list':films})

def film_detail(request, film_id):
    film = Film.objects.get(id=film_id)
    return render(request, 'films_templates/film_detail.html', context={'film':film})

def base(request):
    return render(request, 'base.html')

