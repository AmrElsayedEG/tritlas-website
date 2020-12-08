"""tritlas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from community import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.home_comm),
    path('post/<id>/',views.one_post),
    path('profile/<id>-user/',views.profile_all),
    path('edit-profile/',views.edit_profile),
    path('new/',views.add_post),
    path('login/',LoginView.as_view(template_name='login.html')),
    path('logout/',LogoutView.as_view()),
    path('signup/',views.register),
    #path('reset/', include('django.contrib.auth.urls')),
    path('reset/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path('reset/password_reset/', views.password_reset_request, name="password_reset"),

]
