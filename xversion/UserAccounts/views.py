from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.urls import reverse
from .forms import RegistrationForm, EditProfileForm, DealerRegistrationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from orders.models import UserOrderInfo
from booking.models import CategoryModel
from UserAccounts.models import Feedback
from UserAccounts.forms import FeedbackForm
from django.http import HttpResponse
import datetime


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
    user = get_object_or_404(User, username=request.user)
    rides = UserOrderInfo.objects.filter(u_id=user.id)
    print(rides)
    model_name = []
    for r in rides:
        model = get_object_or_404(CategoryModel, m_id=r.m_id)
        model_name.append(model)
    print(model_name)
    print(user.id)
    args = {
                'user': request.user,
                'message': storage,
                'rides': rides,
                'model': model_name,
         }
    return render(request, 'useraccounts/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST,instance=request.user)
       # profile_form = EditProfileFormCustom(instance=request.user.userprofile,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
           # profile_form.save()

            return redirect('/accounts/profile')
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


def feedback(request):
    form = FeedbackForm()
    context = {
        'form': form,
    }
    return render(request, 'useraccounts/feedback.html', context)


def giveFeedback(request):
    if request.is_ajax() and request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        email = request.POST.get('email')

        review = Feedback()
        review.rating = rating
        review.comment = comment
        review.email = email
        review.pub_date = datetime.datetime.now()
        review.save()
        return HttpResponse(review)
    else:
            print("form invalid")
    return render(request, 'useraccounts/feedback.html')




