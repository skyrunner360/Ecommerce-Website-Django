from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from math import ceil
# Create your views here.
def index(request):
    products = Product.objects.all()
    n= len(products)
    nSlides = n//4 + ceil((n/4) - (n//4))
    params = {'no_of_slides': nSlides,'range': range(1,nSlides),'product': products}
    return render(request,'shop/index.html', params)
def about(request):
    return render(request, 'shop/about.html')
def contact(request):
    return HttpResponse("We are at Contact page")
def tracker(request):
    return HttpResponse("We are at Tracking Page")
def search(request):
    return HttpResponse("We are at Search")
def productview(request):
    return HttpResponse("We are at Product view page")
def checkout(request):
    return HttpResponse("We are at checkout")