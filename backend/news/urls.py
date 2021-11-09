from django.urls import path
from . import views
urlpatterns = [

path('',views.getNews,name='Noticias'),
]