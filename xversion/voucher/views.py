from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from voucher.models import Coupon
from django.contrib.auth.decorators import login_required


@login_required
def cart_coupon(request, coupon_name):
    cc = coupon_name
    print(request.user.ride_count)
    coupon = get_object_or_404(Coupon, coupon_name=cc, status=1)
    if request.user.ride_count is 1:
        if coupon:
            print("applied")
            request.session['coupon'] = cc
            return HttpResponse(request)
    elif request.user.ride_count > 1:
        request.session['coupon'].set_expiry()
        return HttpResponse(request)

