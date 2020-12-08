from django import forms
from django.contrib.auth.models import User

from .models import post, comment, profile


class postForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = post
        fields = ('image','message')

class commentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ('comment',)

class profileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['tell_us_about_yourself','image']

class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']