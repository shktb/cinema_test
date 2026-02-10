from django.http import HttpResponse
from django.shortcuts import render, redirect
from film.models import Film, Category
from film.forms import AddFilmForm
from django.contrib.auth.decorators import login_required

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
    if request.method == "GET":
        films = Film.objects.all()
        category_id = request.GET.get("category_id")
        if category_id:
            films = Film.objects.filter(category_id=category_id)
        return render(request, 'films_templates/film_list.html', context={'list':films})
    
@login_required(login_url="/login/")
def film_create(request):
    if request.method == "GET":
        forms = AddFilmForm()
        return render(request, "films_templates/film_create.html", context={"forms": forms})
    elif request.method == "POST":
        forms = AddFilmForm(request.POST, request.FILES)
        if forms.is_valid():
            Film.objects.create(
                name=forms.cleaned_data.get("name"),
                descriptions=forms.cleaned_data.get("description"),
                year=forms.cleaned_data.get("year"),
                image=forms.cleaned_data.get('image'),
            )
            return redirect("/film/")
        return HttpResponse("error")

@login_required(login_url="/login/")
def film_detail(request, film_id):
    if request.method == "GET":
        film = Film.objects.get(id=film_id)
        return render(request, 'films_templates/film_detail.html', context={'film':film})

def base(request):
    if request.method == "GET":
        category = Category.objects.all()
        return render(request, 'base.html', context={"category" : category})

