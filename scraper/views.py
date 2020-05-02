from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt
from .models import Lookup

from bs4 import BeautifulSoup
import requests
import random
import time
import json

from .objects.google_product import GoogleProduct

GOOGLE_SHOPPING_URL = 'https://www.google.com/search?tbm=shop'

@csrf_exempt 
def index(request):
    if request.method == 'POST':
        body = request.POST
        startUrl = GOOGLE_SHOPPING_URL + '&q=' + body['name']
        startPage = requests.get(startUrl)

        startSoup = BeautifulSoup(startPage.text, 'html.parser')
        productDivs = startSoup.find_all('div', class_='u30d4')

        products = []
        for productDiv in productDivs:
            googleProduct = GoogleProduct(productDiv)
            if googleProduct.price is None:
                continue
            products.append(googleProduct)

        products.sort(key=lambda x: x.price, reverse=True)
        for  i, product in enumerate(products):
            product.calculatePercentile('pricePercentile', i, len(products) - 1)

        products.sort(key=lambda x: x.rating)
        for  i, product in enumerate(products):
            product.calculatePercentile('ratingPercentile', i, len(products) - 1)

        products.sort(key=lambda x: x.reviewCount)
        for  i, product in enumerate(products):
            product.calculatePercentile('reviewCountPercentile', i, len(products) - 1)

        for product in products:
            product.calculateValue(100, 100, 100)

        products.sort(key=lambda x: x.calculatedValue)
        for  i, product in enumerate(products):
            product.calculatePercentile('percentile', i, len(products) - 1)
        products.sort(key=lambda x: x.percentile)

        lookup = Lookup(
            requestIp=get_client_ip(request), 
            name=body['name'], resultUrl=products[-1].url, 
            resultValue=int(products[-1].calculatedValue)
        )
        lookup.save()

        return HttpResponse(json.dumps( [product.__dict__ for product in products] ), content_type="application/json")
    else:
        return render(request, 'scraper/index.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip