from django import forms

from .models import trip, Images


class tripModel(forms.ModelForm):
    class Meta:
        model = trip
        fields = ('destination','date','depart_location','depart_time','nights','phone','place_of_residence','information','contact_and_reservation_info','price')
class ImagesForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Images
        fields = ('image',)