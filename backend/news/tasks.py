from urllib.request import urlopen
from bs4 import BeautifulSoup
from celery import shared_task

from news.models import News

autonomia_financiera_page = 'https://autonomiafinanciera.uautonoma.cl/noticias/'



@shared_task
def giveNews():
  page = urlopen(autonomia_financiera_page)
  soup = BeautifulSoup(page, 'html.parser')
  articles = soup.find_all('article')
  
  return articles