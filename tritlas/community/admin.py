from django.contrib import admin

# Register your models here.
from .models import post,profile,comment

admin.site.register(post)
admin.site.register(profile)
admin.site.register(comment)
