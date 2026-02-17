from django.db import models
from users.models import Profile

# Create your models here.

# ORM Object Relational Mapping

# OneToMany - одна категория - много продуктов
# ManyToMany - много Тэг - много продуктов
# OneToOne - один Пользователь - одна Профиль

# FK - Foreign Key

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
class Genre(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.name}"

class Film(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    year = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True, upload_to='films/')
    genre = models.ManyToManyField(Genre, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    descriptions = models.TextField()

    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.year}"
