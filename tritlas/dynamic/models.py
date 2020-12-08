from django.db import models

# Create your models here.
class Message(models.Model):
    cat = [('طلب إعلان مميز','طلب إعلان مميز'),('اخر','أخر'),('أضف منتجع جديد','أضف منتجع جديد')]
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=70)
    category = models.CharField(max_length=50,choices=cat)
    message = models.TextField()
    date = models.DateField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.name +" - " + str(self.date)

