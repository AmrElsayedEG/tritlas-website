from django.contrib import admin

# Register your models here.
from .models import place,city,place_imgs

admin.site.register(place)
admin.site.register(city)
admin.site.register(place_imgs)