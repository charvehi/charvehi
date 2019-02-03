from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.urls import reverse

from .forms import RegistrationForm, EditProfileForm, DealerRegistrationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

User = get_user_model()
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_vendor:
            return redirect('dealer:show')
        else:
            return redirect('/')
    return render(request, 'useraccounts/home.html')

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid() :
            user =  form.save()
            User.is_active = False#will work from save method in forms
            print("user is",User.is_active)
            messages.success(request,'Register successfull!please login..')
            return redirect('useraccounts:login')
    else:
        form = RegistrationForm()

    args = {'form':form,}
    return render(request,'useraccounts/reg_form.html',args)

#dealer registration form
def registerdealer(request):
    if request.method == 'POST':
        form = DealerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('useraccounts:login')
    else:

        form = DealerRegistrationForm()

    args = {'form': form, }
    return render(request, 'useraccounts/registerdealer_form.html', args)


@login_required
def view_profile(request):
    storage = messages.get_messages(request)

    args = {'user': request.user,'message':storage}
    return render(request,'useraccounts/profile.html',args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST,instance=request.user)
       # profile_form = EditProfileFormCustom(instance=request.user.userprofile,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
           # profile_form.save()

            return redirect('/useraccounts/profile')
    else:
        form = EditProfileForm(instance=request.user)
        #profile_form = EditProfileFormCustom(instance=request.user.userprofile)
        args = {'form': form}
        return render(request,'useraccounts/edit_profile.html',args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your new password has been saved.')
            update_session_auth_hash(request, form.user)
            return redirect(reverse('useraccounts:view_profile'))
        '''else:
            return redirect('/useraccounts/change-password')'''
    else:
        form = PasswordChangeForm(user= request.user)
        args = {'form': form}
        return render(request,'useraccounts/change_password.html',args)



