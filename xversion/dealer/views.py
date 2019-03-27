from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404

from booking.models import CategoryModel
from orders.models import UserOrderInfo
from django.urls import reverse
from django.views.decorators.cache import never_cache
from pandas.core.resample import method
from django.contrib.auth import authenticate, login

from UserAccounts.decorators import dealer_required
from .models import Dealer
from .forms import DealerForm, EditDealerForm, EditModelForm


# Create your views here.
@dealer_required
@login_required
def show(request):
    dealers = Dealer.objects.all().filter(user=request.user)
    dealers1 = Dealer.objects.filter(user=request.user)
    dealer = Dealer.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditDealerForm(request.POST, instance=dealer)
        if form.is_valid():
            form.save()
            print("saving")
            return redirect('dealer:show')

    models_li = []
    models_list = []
    for dl in dealers1:

        category = CategoryModel.objects.all().filter(d_id=dl)
        models_li.append(category)
    print(models_li)
    print(dealers)
    for model in models_li:
        for m in model:
            models_list.append(m)
    form = EditDealerForm(instance=dealer)

    args = {
        'dealers': dealers,
        'models': models_list,
        'media_url': settings.MEDIA_URL,
        'form': form,
         }
    return render(request, "dealer/detailshow.html", args)

@dealer_required
@login_required
def edit(request, id):
    model = CategoryModel.objects.get(m_id=id)
    return render(request,'dealer/edit1.html', {'model':model})
@dealer_required
@login_required
def update(request, id):
    model = CategoryModel.objects.get(m_id=id)
    form = EditModelForm(request.POST, instance = model)
    if form.is_valid():
        u = form.save()
        u.save()
        print("saving")
        return redirect('dealer:show')
    return render(request, 'dealer/edit1.html', {'category': model})


@login_required
def rides(request):
    dealer = get_object_or_404(Dealer, user=request.user)
    rides = UserOrderInfo.objects.filter(d_id=dealer.d_id, due=True)
    print(dealer.d_id)
    args = {
                'rides': rides,
         }
    return render(request, "dealer/ridedetail.html", args)
