from django.shortcuts import render, render_to_response
from django.http import HttpResponse
# Create your views here.
from .forms import messageForm
from .models import Message


def home(request):
    return render(request,'index.html',context={'nbar': 'home'})
def who(request):
    return render(request,'who.html',context={'nbar': 'who'})
def contact(request):
    if request.method == 'POST':
        form = messageForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'تم إرسال الرسالة وسنتواصل معكم قريباً'
            msg_eng = 'Your message has been successfully sent. We will contact you very soon! Thank you for contacting us.'
    else:
        form = messageForm()
        msg = None
        msg_eng = None
    context = {
        'form':form,
        'msg':msg,
        'msg_eng' :msg_eng,
        'nbar': 'contact',
    }
    return render(request,'contact.html',context)

from django.views.defaults import page_not_found
def handler_404(request, exception):
    return page_not_found(request, exception, template_name="400.html")
