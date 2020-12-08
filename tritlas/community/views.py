from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from trips.models import tripAd, trip
# Create your views here.
from .forms import postForm, commentForm, userForm, profileForm
from .models import post, comment, profile
from django.contrib.auth import login,authenticate

#trip ads


def trip_ad():
    trips = tripAd.objects.all().exclude(published=False)
    try:
        min_ind = trips[0].view_time
        f_id = None
        for i in trips:
            if i.view_time <= min_ind:
                min_ind = i.view_time
                f_id = i.id
        try:
            target = tripAd.objects.get(id=f_id)
            target.view_time += 1
            target.save()
        except:
            target = None
    except:
        target = None
    return target


def home_comm(request):
    all_postss = post.objects.all()
    all_posts = all_postss[::-1]
    paginator = Paginator(all_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'all_posts':all_posts,
        'page_obj':page_obj,
        'nbar': 'community',
    }
    return render(request,'comm.html',context)
def one_post(request,id):
    o_post = post.objects.get(id=id)
    all_commentss = comment.objects.filter(in_post=id)
    all_comments = all_commentss[::-1]
    can_delete = False
    #Ads
    ad = trip_ad()
    if str(o_post.user) == str(request.user):
        can_delete = True
    if request.method == 'POST':
        if 'delete_this' in request.POST:
            o_post.delete()
            form = commentForm()
            return redirect('/community/')
        else:
            form = commentForm(request.POST)
            if form.is_valid():
                ccomment = form.cleaned_data['comment']
                user = request.user
                obj = comment.objects.create(in_post=o_post,user=profile.objects.get(user=user),comment=ccomment)
                obj.save()
                o_post.comment_counter += 1
                o_post.save()
                return redirect('/community/post/%s' %(o_post.id))
    else:
        form = commentForm()
    context = {
        'o_post':o_post,
        'all_comments':all_comments,
        'form':form,
        'can_delete':can_delete,
        'ad':ad,
        'nbar': 'community',
    }
    return render(request,'comm-one-post.html',context)

def edit_profile(request):
    current_user = request.user
    current_img = profile.objects.get(user=request.user)
    user_profile = get_object_or_404(profile,user=current_user)
    if request.method == 'POST':
        user_form = userForm(request.POST,instance=request.user)
        profile_form = profileForm(request.POST,request.FILES,instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            new_profile = profile_form.save(commit=False)
            new_profile.save()
            return redirect('/community/profile/%s-user' %(current_user.id))
    else:
        user_form = userForm(instance=request.user)
        profile_form = profileForm(instance=user_profile)
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'current_img':current_img,
        'nbar': 'community',
    }
    return render(request,'edit-profile.html',context)
@login_required
def add_post(request):
    if request.method == 'POST':
        form = postForm(request.POST, request.FILES)
        if form.is_valid():
            mess = form.cleaned_data['message']
            img = form.cleaned_data['image']
            obj = post.objects.create(user=profile.objects.get(user=request.user),
                                      message=mess,
                                      image=img)
            obj.save()
            return redirect('/community/post/%s' %(obj.id))
    else:
        form = postForm()
    context = {
        'form':form,
        'nbar': 'community',
    }
    return render(request,'add-post.html',context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('/community/edit-profile')
    else:
        form = UserCreationForm()
    context = {
        'form':form,
        'nbar': 'community',
    }
    return render(request,'signup.html',context)

def profile_all(request,id):
    edit = False
    user_profile = get_object_or_404(profile,id=id)
    user_tripss = trip.objects.filter(user=id)
    user_trips = user_tripss[::-1]
    user_postss = post.objects.filter(user=id)
    user_posts = user_postss[::-1]
    try:
        if request.user == user_profile.user:
            edit = True
    except:
        edit = False
    try:
        view_msg = request.session.get('pop_msg')
        del request.session['pop_msg']
    except:
        view_msg = False
    context = {
        'user_profile' : user_profile,
        'edit':edit,
        'nbar': 'community',
        'user_trips':user_trips,
        'user_posts':user_posts,
        'view_msg':view_msg
    }
    return render(request,'profile.html',context)
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "password/password_reset_subject.txt"
                        c = {
					    "email":user.email,
					    'domain':'www.tritlas.com',
					    'site_name': 'TriTlas | Egypt',
					    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
					    "user": user,
					    'token': default_token_generator.make_token(user),
					    'protocol': 'http',
					    }
                        email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/community/reset/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

