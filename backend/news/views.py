from urllib.request import urlopen
from bs4 import BeautifulSoup, BeautifulStoneSoup
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from news.models import News
from news.tasks import giveNews

autonomia_financiera_page = 'https://autonomiafinanciera.uautonoma.cl/noticias/'


def getArticleData(article):
    img = article.find('img')['src']

    title = article.div.h2
    titleString = title.string

    link = article.div.h2.a['href']

    date = article.find('time')
    dateString = date.string

    category = date.next_sibling
    categoryString = category.string

    description = title.next_sibling.next_sibling.string

    return {'img': img, 'title': titleString, 'link': link, 'date': dateString, 'category': categoryString, 'description': description}

def formatPage(page):
    
    soup = BeautifulSoup(page, 'html.parser')
    news = soup.find_all('article')
    formatedNews = []
    for new in news:
        newFormated = getArticleData(new)
        newCopy = newFormated.copy()
        formatedNews.append(newCopy)
    return formatedNews
# Create your views here.
@api_view(['GET'])
def getNews(request):
    page = urlopen(autonomia_financiera_page)
    pageFormated = formatPage(page)
    return HttpResponse([pageFormated])
