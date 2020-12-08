from django.contrib import admin

# Register your models here.
from .models import trip,Images,tripAd

admin.site.register(trip)
admin.site.register(Images)
admin.site.register(tripAd)