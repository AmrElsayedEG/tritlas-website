from django.db import models
from django.template.defaultfilters import slugify
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import sys
from django.db.models.signals import post_save
# Create your models here.
class city(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='city-imgs')
    num_of_places =  models.IntegerField(default='0',blank=True,null=True)
    def __str__(self):
        return self.name

class place(models.Model):
    name = models.CharField(max_length=100)
    in_city = models.ForeignKey(city,on_delete=models.CASCADE)
    info = models.TextField(blank=True,null=True)
    img = models.ImageField(upload_to='city-imgs',blank=True,null=True)
    distant = models.CharField(max_length=10,default='غير محدد')
    address = models.CharField(max_length=300,default='غير محدد',blank=True,null=True)
    source = models.CharField(max_length=300,default='http://www.tritlas.com/',blank=True,null=True)

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        im = Image.open(self.img)

        output = BytesIO()

        # Resize/modify the image
        #im = im.resize((100, 100))

        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=70)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.img = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.img.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

        super(place, self).save()
    
    def __str__(self):
        return self.name


class place_imgs(models.Model):
    place = models.ForeignKey(place,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='place-imgs')
    
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

        super(place_imgs, self).save()
        
    def __str__(self):
        return self.place.name

def update_thread(sender, **kwargs):
        instance = kwargs['instance']
        created = kwargs['created']
        raw = kwargs['raw']
        if created and not raw:
            instance.in_city.num_of_places += 1
            instance.in_city.save()
post_save.connect(update_thread, sender=place)
