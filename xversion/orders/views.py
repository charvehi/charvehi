from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import UserOrderInfo
from booking.models import CategoryModel
from .cart import Cart
import datetime
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt

#---------------------Payments views begin--------------------------#
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template, RequestContext
import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf


def Home(request):
    cart = Cart(request)
    MERCHANT_KEY = "xoTYBwdz"
    key = "xoTYBwdz"
    SALT = "XPR2AS7dy8"
    PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
    action = ''
    posted = {}
    phone = request.POST.get('phone', '')
    firstname = request.POST.get('firstname')
    # Merchant Key and Salt provided y the PayU.
    for i in request.POST:
        posted[i] = request.POST[i]
    hash_object = hashlib.sha256(b'randint(0,20)')
    txnid = hash_object.hexdigest()[0:20]
    hashh = ''
    posted['txnid'] = txnid

    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    posted['key'] = key
    hash_string = ''
    hashVarsSeq = hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string += str(posted[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += SALT
    hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    action = PAYU_BASE_URL
    if (posted.get("key") != None and posted.get("txnid") != None and posted.get("productinfo") != None and posted.get(
            "firstname") != None and posted.get("email") != None):
        args = {
            "phone": phone,
            "firstname": firstname,
            "cart": cart,
            "posted": posted, "hashh": hashh,
            "MERCHANT_KEY": MERCHANT_KEY,
            "txnid": txnid,
            "hash_string": hash_string,
            "action": PAYU_BASE_URL,
        }
        return render(request, 'orders/current_datetime.html', args)
    else:
        args = {
            "phone": phone,
            "firstname": firstname,
            "cart": cart,
            "posted": posted, "hashh": hashh,
            "MERCHANT_KEY": MERCHANT_KEY,
            "txnid": txnid,
            "hash_string": hash_string,
            "action": ".",
        }
        return render(request, 'orders/current_datetime.html', args)


@csrf_protect
@csrf_exempt
def success(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "GQs7yium"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print
        "Thank You. Your order status is ", status
        print
        "Your Transaction ID for this transaction is ", txnid
        print
        "We have received a payment of Rs. ", amount, ". Your order will soon be shipped."

    #------------------------------save order in DB---------------------------#
    cart = Cart(request)
    start = request.COOKIES.get('start')
    end = request.COOKIES.get('end')
    days, hours, minutes, net_hours = duration_calc(request, start, end)

    d_li = []
    m_li = []
    price_hour_dealer_li = []
    price_day_dealer_li = []
    dealer_money_li = []

    for item in cart:
        dealer = item['model'].d_id.d_id
        model = item['model'].m_id
        dealer_hour_price = item['model'].price_hour_dealer
        dealer_day_price = item['model'].price_day_dealer
        dealer_amount = dealer_money(request, item['model'], days, hours, minutes, net_hours)

        d_li.append(dealer)
        m_li.append(model)
        price_hour_dealer_li.append(dealer_hour_price)
        price_day_dealer_li.append(dealer_day_price)
        dealer_money_li.append(dealer_amount)

    for d_id, m_id, price_h_dealer, price_d_dealer, money_dealer, item in zip(d_li, m_li, price_hour_dealer_li, price_day_dealer_li, dealer_money_li, cart):
        orders = UserOrderInfo()
        print("delivery value is")
        print(item['delivery'])
        if item['delivery'] is 1:
            orders.delivery = 1
        else:
            orders.delivery = 0

        if request.user.id is None:
            orders.u_id = 0
        else:
            orders.u_id = request.user.id

        orders.order_id = txnid
        orders.u_id = orders.u_id
        orders.name = request.POST["firstname"]
        orders.mobile = request.POST["phone"]
        orders.d_id = d_id
        orders.m_id = m_id
        orders.booked_at = datetime.datetime.now()
        orders.start_date = datetime.datetime.strptime(request.COOKIES.get('start').split(" ", 1)[0], '%d/%m/%Y').strftime('%Y-%m-%d')
        orders.start_time = request.COOKIES.get('start').split(" ", 1)[1]
        orders.end_date = datetime.datetime.strptime(request.COOKIES.get('end').split(" ", 1)[0], '%d/%m/%Y').strftime('%Y-%m-%d')
        orders.end_time = request.COOKIES.get('end').split(" ", 1)[1]
        orders.duration = str(days)+"::"+str(hours)+":"+str(minutes)+"("+str(net_hours)+")"
        orders.delivery = orders.delivery
        orders.price_hour = price_h_dealer
        orders.price_day = price_d_dealer
        orders.dealer_money = money_dealer
        orders.amount_paid = request.POST["amount"]
        orders.lat = request.COOKIES.get('lat')
        orders.lon = request.COOKIES.get('lon')

        models = CategoryModel.objects.get(m_id=item['model'].m_id)
        models.status = 0
        models.save()
        orders.save()
    cart.clear()
    #------------------------------save order in DB ends-------------------------------#

    args = {
        "txnid": txnid,
        "status": status,
        "amount": amount,
    }
    return render(request, 'orders/success.html', args)


@csrf_protect
@csrf_exempt
def failure(request):
    c = {}
    cart = Cart(request)
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = ""
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        print
        "Invalid Transaction. Please try again"
    else:
        print
        "Thank You. Your order status is ", status
        print
        "Your Transaction ID for this transaction is ", txnid
        print
        "We have received a payment of Rs. ", amount, ". Your order will soon be shipped."

    return render(request, "orders/Failure.html", c)
#---------------------Payments views ends--------------------------#


def duration_calc(request, start, end):
    datetimeFormat1 = '%d/%m/%Y %I:%M %p'
    check = dt.strptime(start, datetimeFormat1)
    check.strftime('%d/%m/%Y %H:%M')


    check1 = dt.strptime(end, datetimeFormat1)
    check1.strftime('%d/%m/%Y %H:%M')
    newdiff = check1 - check
    days, hours, minutes = newdiff.days, newdiff.seconds // 3600, newdiff.seconds % 3600 / 60.0
    print(hours)
    net_hours = (days*24)+hours
    print(net_hours)
    return days, hours, minutes, net_hours


@login_required
def order_report(request):
    orders = UserOrderInfo.objects.all()
    print(datetime.date.today())
    order =None
    if request.GET.get('from', '') and request.GET.get('to', ''):
        from_date = request.GET.get('from', '')
        to_date = request.GET.get('to', '')
        if request.GET.get('order_id', ''):
            order_id = request.GET.get('order_id', '')
            order = UserOrderInfo.objects.filter(booked_at__range=[from_date, to_date], order_id=order_id)  # Y-m-d
        elif request.GET.get('user_id', ''):
            user_id = request.GET.get('user_id', '')
            order = UserOrderInfo.objects.filter(booked_at__range=[from_date, to_date], u_id=user_id)  # Y-m-d
        elif request.GET.get('dealer_id', ''):
            dealer_id = request.GET.get('dealer_id', '')
            order = UserOrderInfo.objects.filter(booked_at__range=[from_date, to_date], d_id=dealer_id)  # Y-m-d
        elif request.GET.get('model_id', ''):
            model_id = request.GET.get('model_id', '')
            order = UserOrderInfo.objects.filter(booked_at__range=[from_date, to_date], m_id=model_id)  # Y-m-d

    context = {
        'order': order,
        'orders': orders,
    }
    return render(request, 'ad_protected/order_report.html', context)


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    net_price=item['net_price'],
                    quantity=item['quantity'],
                )
            cart.clear()
        return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'form': form})


#@require_POST
def cart_add(request, model_id, model_slug=None):
    loc = request.GET.get('current_loc', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    lat = float(request.GET.get('lat', ''))
    lon = float(request.GET.get('lon', ''))

    cart = Cart(request)
    if model_slug:
        model = get_object_or_404(CategoryModel, m_id=model_id)
        #cart['quantity'] = 1
        cart.add(request, model=model, quantity=1)

    response = redirect('orders:cart_detail')
    response.set_cookie('loc', loc)
    response.set_cookie('start', start)
    response.set_cookie('end', end)
    response.set_cookie('lat', lat)
    response.set_cookie('lon', lon)

    return response
    #return render(request, 'orders/order_list.html', {'cart': cart})


def cart_remove(request, model_id):
    cart = Cart(request)
    product = get_object_or_404(CategoryModel, m_id=model_id)
    cart.remove(product)
    return redirect('orders:cart_detail')


def cart_detail(request):
    cart = Cart(request)

    loc = request.COOKIES.get('loc')
    start = request.COOKIES.get('start')
    end = request.COOKIES.get('end')
    lat = request.COOKIES.get('lat')
    lon = request.COOKIES.get('lon')

    s = "15/03/2019 12:30 PM"
    print("string is")
    print(s.split(" ", 1)[1])

    d_li = []
    m_li = []
    for item in cart:
        model = item['model'].price_hour_dealer
        dealer = item['model'].d_id.d_id
        d_li.append(dealer)
        m_li.append(model)
    print(d_li)
    print(m_li)

    if request.session.get('coupon', None):
        coupon_name = request.session['coupon']
    else:
        coupon_name = None
    coupon = request.GET.get('coupon', '')

    if request.user.is_authenticated:
        if request.user.ride_count is 0:
            coupon_name = None

    #for item in cart:
     #   item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    context = {
        'media_url': settings.MEDIA_URL,
        'cart': cart,
        'loc': loc,
        'start': start,
        'end': end,
        'lat': lat,
        'lon': lon,
        'coupon_value': coupon_name,
        'coupon': coupon,
    }
    return render(request, 'orders/order_list.html', context)


def dealer_money(request, models, days, hours, minutes, net_hours):
    priceHour = models.price_hour_dealer
    PH_Count = models.ph_count
    priceDay = models.price_day_dealer
    PD_count = models.pd_count

    print(priceHour)
    print(priceDay)

    min_factor = 0
    if int(minutes) is not 0:
        min_factor = 1

    if PD_count is 1:
        PD_count = 12
    else:
        PD_count = 24

    if PD_count >= net_hours > PH_Count:
        dealer_money = (float(priceDay))

    elif net_hours >= PD_count:
        dealer_money = ((float(priceDay)) * (int(net_hours / PD_count))) + (float(priceHour) * \
                int(net_hours % PD_count)) + ((float(priceHour) / 2) * min_factor)

    elif net_hours < PD_count:
        dealer_money = int(net_hours) * float(priceHour) + ((float(priceHour) / 2) * min_factor)

    print(dealer_money)
    return dealer_money


def delivery_charge(request, model_id, delivery_value):
    print("entered del")
    dv = delivery_value
    print(dv)
    cart = Cart(request)
    product = get_object_or_404(CategoryModel, m_id=model_id)
    #d_charge = get_object_or_404(CategoryModel, is_delivery=True)
    if dv is '1':
        print("applied")
        cart.add_delivery(product)
        return HttpResponse(request)
    elif dv is '0':
        cart.remove_delivery(product)
        return HttpResponse(request)


