"""tritlas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from cities import views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)
from . import api
urlpatterns = [
    path('',views.all_cities),
    path('<id>',views.one_city),
    path('place/<id>',views.one_place),
    path('api/doc',views.api_doc),
    path('api/place',api.PlaceDetail.as_view(),name='placeapi'),
    path('api/place/<int:id>',api.OnePlaceDetail.as_view(),name='oneplaceapi'),
    path('api/city',api.CityDetail.as_view(),name='cityapi'),
    path('api/city/<int:id>',api.OneCityDetail.as_view(),name='onecityapi')
]
