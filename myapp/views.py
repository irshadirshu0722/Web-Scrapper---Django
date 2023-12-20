from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect
from .models import Link

# Create your views here.

def scraper(request):
  if request.method =="POST":
    site = request.POST.get('site','')
    types = request.POST.get('type','a')
    page = requests.get(site)
    soup = BeautifulSoup(page.text,'html.parser')
    for link in soup.find_all(types):
      tag = 'href' if types== 'a' else 'src'
      link_address = link.get(tag)
      link_text = link.string
      Link.objects.create(address = link_address,name=link_text,type=types)
    return HttpResponseRedirect('/')
  else:

    data = Link.objects.all()[::-1]

  return render(request,'myapp/result.html',{'link_address':data})


def clear(request):
  Link.objects.all().delete()
  return HttpResponseRedirect('/')



