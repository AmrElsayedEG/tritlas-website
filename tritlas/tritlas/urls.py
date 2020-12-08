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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from tritlas import settings
from django.conf.urls import (
handler400, handler403, handler404, handler500
)
from rest_framework.authtoken import views
urlpatterns = [
    path('tritlas-main-admin/', admin.site.urls),
    path('',include('dynamic.urls')),
    path('city/',include('cities.urls')),
    path('trips/',include('trips.urls')),
    path('community/',include('community.urls')),
    re_path('djga/', include('google_analytics.urls')),
    path('api-auth/', include('rest_framework.urls')), #api
    path('api-token-auth/', views.obtain_auth_token), #api
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'dynamic.views.handler_404'
