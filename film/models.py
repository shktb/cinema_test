from django.db import models

# Create your models here.

# ORM Object Relational Mapping
class Film(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(default=0)
    genre = models.CharField(max_length=255)
    descriptions = models.TextField()
