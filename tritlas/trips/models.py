from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import sys
# Create your models here.
class trip(models.Model):
    user = models.ForeignKey('community.profile', on_delete=models.CASCADE,blank=True,null=True)
    destination = models.ForeignKey('cities.city',on_delete=models.CASCADE)
    date = models.DateField(default='2020-12-30')
    depart_location = models.CharField(max_length=25)
    depart_time = models.CharField(max_length=6)
    nights = models.IntegerField()
    phone = models.CharField(max_length=18)
    place_of_residence = models.CharField(max_length=20)
    information = models.TextField()
    contact_and_reservation_info = models.TextField()
    price = models.IntegerField()
    active = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    boost = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " --- " + str(self.destination)


class Images(models.Model):
    post = models.ForeignKey(trip, default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post-image')

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        im = Image.open(self.image)

        output = BytesIO()

        # Resize/modify the image
        #im = im.resize((100, 100))

        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=70)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

        super(Images, self).save()

class tripAd(models.Model):
    trip_ad = models.ForeignKey(trip, default=None,on_delete=models.CASCADE)
    view_time = models.IntegerField(default=0)
    published = models.BooleanField(default=False)

    def __str__(self):
        return str(self.trip_ad)
