from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader
from .models import city,place,place_imgs
from trips.models import trip
from django.core.paginator import Paginator

# Create your views here.



def all_cities(request):
    cities = city.objects.all()
    paginator = Paginator(cities, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj,
        'nbar': 'city',
    }
    return render(request,'cities.html',context)
def one_city(request,id):
    places = None
    cities = None
    city_name = 'غير متواجد'
    page_obj = None
    boost_trips = trip.objects.filter(destination=id, boost=True).exclude(published=False)
    all_trips = trip.objects.filter(destination=id).exclude(published=False)
    try:
        places = place.objects.filter(in_city=id)
        cities = city.objects.get(id=id)
        city_name = cities
        paginator = Paginator(places, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except:
        all_trips = trip.objects.filter(destination=id).exclude(published=False)
    print(cities)
    context = {
        'places' : places,
        'city_name':city_name,
        'cities':cities,
        'all_trips':all_trips,
        'boost_trips':boost_trips,
        'page_obj':page_obj,
        'nbar': 'city',
    }
    return render(request,'one-city.html',context)
def one_place(request,id):
    one = place.objects.get(id=id)
    one_img = place_imgs.objects.filter(place=id)
    links = []
    for i in range(0,len(one_img)):
        links.append(one_img[i].image)
    context = {
        'one':one,
        'links':links,
        'nbar': 'city',
    }
    return render(request,'place.html',context)


#API
from django.contrib.auth.decorators import login_required
@login_required
def api_doc(request):
    return render(request,'api-doc.html')

