import math

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q

from film.models import Film, Category
from film.forms import AddFilmForm, SearchForm

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, DeleteView, TemplateView

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
# FBV
# CBV

class FilmListView(ListView):
    model = Film
    template_name = "films_templates/film_list.html"
    context_object_name = "list"
    paginate_by = 3

    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(descriptions__icontains=search))
        category_id = self.request.GET.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        year_choice = self.request.GET.get("year_choice")
        if year_choice:
            if year_choice == "1":
                queryset = queryset.filter(year__gt=2000)
            elif year_choice == "2":
                queryset = queryset.filter(year__lt=2000)
            elif year_choice == "0":
                None
        for_test = self.request.GET.get("for_test")
        if for_test:
            if for_test == "1":
                queryset = queryset.filter(genre__name="Комедия")
            if for_test == "2":
                queryset = queryset.filter(genre__name="Фэнтези")
        genre = self.request.GET.getlist("genre")
        if genre:
            queryset = queryset.filter(genre__in=genre)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forms"] = SearchForm()
        return context
    
class FilmCreateView(LoginRequiredMixin, CreateView):
    model = Film
    form_class = AddFilmForm
    template_name = "films_templates/film_create.html"
    success_url = reverse_lazy("film_list")

    login_url = "/login/"

    def form_valid(self, form):
        film = form.save(commit=False)
        if hasattr(self.request.user, 'profile'):
            film.profile = self.request.user.profile
        film.save()
        return super().form_valid(form)
    
class FilmDetailView(LoginRequiredMixin, DetailView):
    model = Film
    template_name = "films_templates/film_detail.html"
    context_object_name = "film"
    pk_url_kwarg = "film_id"

    login_url = "/login/"
    
class FilmDeleteView(LoginRequiredMixin, DeleteView):
    model = Film
    success_url = reverse_lazy("film_list")
    template_name = "films_templates/film_confirm_delete.html"
    pk_url_kwarg = "film_id"

    login_url = "/login/"
    
    def dispatch(self, request, *args, **kwargs):
        film = self.get_object()
        if request.user.profile != film.profile:
            return HttpResponse("Permission denied")
        return super().dispatch(request, *args, **kwargs)
    
class BaseView(TemplateView):
    template_name = "base.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context
    



def film_list(request):

    limit = 3

    if request.method == "GET":
        films = Film.objects.all()
        forms = SearchForm()
        if request.GET.get("search"):
            search = request.GET.get("search")

            films = Film.objects.filter( Q (name__icontains=search) | Q (descriptions__icontains=search))
        category_id = request.GET.get("category_id")
        if category_id:
            films = Film.objects.filter(category_id=category_id)
        year_choice = request.GET.get("year_choice")
        if year_choice:
            if year_choice == "1":
                films = Film.objects.filter(year__gt=2000)
            elif year_choice == "2":
                films = Film.objects.filter(year__lt=2000)
            elif year_choice == "0":
                None
        for_test = request.GET.get("for_test")
        if for_test:
            if for_test == "1":
                films = Film.objects.filter(genre__name="Комедия")
            if for_test == "2":
                films = Film.objects.filter(genre__name="Фэнтези")
        genre = request.GET.getlist("genre")
        if genre:
            films = Film.objects.filter(genre__in=genre)

        page = int(request.GET.get("page")) if request.GET.get("page") else 1
        max_page = math.ceil(len(films) / limit)
        start = (page - 1) * limit
        stop = page * limit
        list_pages = range(1, max_page + 1)
        films = films[start:stop]

        return render(request, 'films_templates/film_list.html', context={'list':films, "forms": forms, "list_pages": list_pages})
    
@login_required(login_url="/login/")
def film_create(request):
    if request.method == "GET":
        forms = AddFilmForm()
        return render(request, "films_templates/film_create.html", context={"forms": forms})
    elif request.method == "POST":
        forms = AddFilmForm(request.POST, request.FILES)
        if forms.is_valid():
            Film.objects.create(
                profile=request.user.profile,
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
    
def film_delete(request, film_id):
    film = Film.objects.get(id=film_id)
    if request.user.profile != film.profile:
        return HttpResponse("Permission denied")
    film.delete()
    return redirect("/film/")



# def base(request):
#     if request.method == "GET":
#         category = Category.objects.all()
#         return render(request, 'base.html', context={"category" : category})

