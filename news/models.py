from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField()
    description = models.CharField()
    image = models.CharField()
    link = models.CharField()
    category = models.CharField()
    date = models.CharField()