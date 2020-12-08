from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from cities.models import city
# Create your views here.
from .forms import tripModel, ImagesForm
from .models import trip, Images
from community.models import profile


def one_trip(request):
    city_list = city.objects.all()
    city_name = False
    trip_boost = False
    trip_list_1 = False
    all_trip_boostt = trip.objects.filter(boost=True).exclude(published=False)
    try:
        all_trip_boost = all_trip_boostt[::-1]
    except:
        all_trip_boost = all_trip_boostt
    if request.GET:
        all_trip_boost = None
        city_name = request.GET.get("city","")
        trip_boostt = trip.objects.filter(destination=city_name,boost=True).exclude(published=False)
        trip_boost = trip_boostt[::-1]
        trip_list_1 = trip.objects.filter(destination=city_name).exclude(boost=True)
        trip_listt = trip_list_1.exclude(published=False)
        trip_list = trip_listt[::-1]
    else:
        trip_listt = trip.objects.all().exclude(boost=True).exclude(published=False)
        try:
            trip_list = trip_listt[::-1]
        except:
            trip_list = trip_listt
    try:
        paginator = Paginator(trip_list, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = None
    context = {
        'city_list' : city_list,
        'trip_list' : trip_list,
        'trip_boost': trip_boost,
        'all_trip_boost':all_trip_boost,
        'city_name':city_name,
        'nbar': 'trip',
        'page_obj':page_obj
    }
    return render(request,'trip-place.html',context)

def view_trip(request,id):
    trips = trip.objects.get(id=id)
    img = Images.objects.filter(post=id)
    imgs = []
    author = False
    if str(trips.user) == str(request.user):
        author = True
    for i in range(0,len(img)):
        imgs.append(img[i].image)
    if request.method == 'GET':
        if 'stop' in request.GET:
            trips.active = False
            trips.save()
        if 'ret' in request.GET:
            trips.active = True
            trips.save()
        if 'del' in request.GET:
            trips.delete()
            return redirect('/trips/')

    context = {
        'trips':trips,
        'imgs':imgs,
        'nbar': 'trip',
        'author':author
    }
    return render(request,"one-trip.html",context)

@login_required
def add_trip(request):
    ImageFormSet = modelformset_factory(Images,form=ImagesForm, extra=3)
    if request.method == 'POST':
        pForm = tripModel(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,queryset=Images.objects.none())
        if pForm.is_valid() and formset.is_valid():
            f_dist = pForm.cleaned_data['destination']
            f_date = pForm.cleaned_data['date']
            f_depart_loc = pForm.cleaned_data['depart_location']
            f_depart_time = pForm.cleaned_data['depart_time']
            f_nights = pForm.cleaned_data['nights']
            f_phone = pForm.cleaned_data['phone']
            f_stay_place = pForm.cleaned_data['place_of_residence']
            f_info = pForm.cleaned_data['information']
            f_contact = pForm.cleaned_data['contact_and_reservation_info']
            f_price = pForm.cleaned_data['price']
            t = trip(user=profile.objects.get(user=request.user),destination=f_dist,date=f_date,depart_location=f_depart_loc,depart_time=f_depart_time,nights=f_nights,phone=f_phone,place_of_residence=f_stay_place,information=f_info,contact_and_reservation_info=f_contact,price=f_price)
            #post_form = pForm.save(commit=False)
            #post_form.save()
            t.save()
            for form in formset.cleaned_data:
                image = form['image']
                photo = Images(post=t, image=image)
                photo.save()
            request.session['pop_msg'] = True
            return redirect('/community/profile/%s-user' %(request.user.id))
        else:
            print(pForm.errors, formset.errors)
    else:
        pForm = tripModel()
        formset = ImageFormSet(queryset=Images.objects.none())

    context = {'pForm': pForm, 'formset': formset,'nbar': 'trip'}
    return render(request,'add-trip.html',context)

def select(request):
    return render(request,'select.html',context={'nbar': 'trip'})
