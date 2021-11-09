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
    dateString = article.find('time').string

    category = date.next_sibling
    categoryString = date.next_sibling.string

    description = article.h2.next_sibling.next_sibling.string

    return {'img': img, 'title': titleString, 'link': link, 'date': dateString, 'category': categoryString, 'description': description}


# Create your views here.
@api_view(['GET'])
def getNews(request):
    page = urlopen(autonomia_financiera_page)
    soup = BeautifulSoup(page, 'html.parser')
    articles = soup.find_all('article')
    returnedArticles = []
    for article in articles:
        articleFormated = getArticleData(article)
        articleCopy = articleFormated.copy()
        returnedArticles.append(articleCopy)
    print(returnedArticles)
    return HttpResponse([returnedArticles])
