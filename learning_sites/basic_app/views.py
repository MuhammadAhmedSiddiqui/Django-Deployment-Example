from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
# Create your views here.

@login_required
def index(request):
    return render(request,'basic_app/index.html')

def registration(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',{'user_form': user_form, 'profile_form':profile_form,'registered':registered})



def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('basic_app:index'))
            else:
                return HttpResponse('Account is not Activated')
        else:
            return HttpResponse('Invalid Username OR password')
    else:
        return render(request,'basic_app/login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))
