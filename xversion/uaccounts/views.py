from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileInfoForm
from .models import UserProfileInfo
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import auth


def index(request):
    if request.session._session:
        return render(request, 'booking/aindex/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    user = UserForm(data=request.POST)
    user_form = UserProfileInfoForm(request.POST or None)
    if user_form.is_valid() and user.is_valid():
        user_form.save()

    context = {'user': user, 'form': user_form}
    #login(request, user)
    return render(request, 'uaccounts/signup.html', context)


def user_login(request):
    email = None

    form = UserProfileInfoForm()
    if request.method == 'GET':
        if 'email' in request.session:
            email = request.session['email']

    elif request.method == 'POST':
        form = UserProfileInfoForm(request.POST or None)
        if form.is_valid():
            #cd = form.cleaned_data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            email = request.POST.get("email")
            password = request.POST.get("password")
            print(email)
            user = auth.authenticate(email=email, password=password)
            print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user.is_authenticated = True
                    request.session['email'] = email
                    request.session.set_expiry(300)
                    #return HttpResponseRedirect(reverse('index'))
                    #request.session.set_expiry(300)
                else:
                    email = None
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(email, password))
                return HttpResponse("User is none......Invalid login details. Try again.")
        else:
            return HttpResponse("Form Invalid.")

    if email is not None:
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'uaccounts/signin.html', {'email': email})


def user_logout(request):
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET.get('action')
            if action == 'logout':
                if request.session.has_key('email'):
                    request.session.flush()
                #return redirect('uaccounts:user_logout')
        return render(request, 'uaccounts/signin.html')
'''
def index(request):
    return render(request,'uaccounts/home.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST or None)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_photos' in request.FILES:
                print('found it')
                profile.profile_photos = request.FILES['profile_photos']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'uaccounts/signup.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details. Try again.")
    else:
        return render(request, 'uaccounts/signin.html', {})
'''