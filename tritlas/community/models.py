from datetime import datetime
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import sys
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    tell_us_about_yourself = models.TextField()
    image = models.ImageField(upload_to='users')
    joined_date = models.DateField(auto_now=True,blank=True)
    slug = models.SlugField(null=True,blank=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.first_name)
        super(profile,self).save(*args,**kwargs)
    def __str__(self):
        return '%s' % (self.user)

class post(models.Model):
    user = models.ForeignKey(profile,on_delete=models.CASCADE)
    message = models.TextField(max_length=120)
    date = models.DateTimeField(default=datetime.now, blank=True)
    image = models.ImageField(upload_to='post-imgs')
    comment_counter = models.IntegerField(default=0, blank=True)

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

        super(post, self).save()
    
    def __str__(self):
        return str(self.date)

class comment(models.Model):
    in_post = models.ForeignKey(post,on_delete=models.CASCADE)
    user = models.ForeignKey(profile, on_delete=models.CASCADE)
    comment = models.TextField(max_length=120)
    date = models.DateTimeField(default=datetime.now, blank=True)



def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile = profile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile,sender=User)
