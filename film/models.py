from django.db import models

# Create your models here.

# ORM Object Relational Mapping
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Film(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(default=0)
    genre = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    descriptions = models.TextField()

    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name
