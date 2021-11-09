from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1500)
    image = models.CharField(max_length=600)
    link = models.CharField(max_length=600)
    category = models.CharField(max_length=60)
    date = models.CharField(max_length=20)