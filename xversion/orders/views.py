from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import UserOrderInfo
from booking.models import CategoryModel
from .cart import Cart
import datetime
from django.contrib.auth.decorators import login_required

#---------------------Payments views begin--------------------------#
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template, RequestContext
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf


def Home(request):
    MERCHANT_KEY = "xoTYBwdz"
    key = "xoTYBwdz"
    SALT = "XPR2AS7dy8"
    PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
    action = ''
    posted = {}
    # Merchant Key and Salt provided y the PayU.
    for i in request.POST:
        posted[i] = request.POST[i]
    random = str(randint(0, 20))

    hash_object = hashlib.sha256(random)
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
        args = {"posted": posted, "hashh": hashh,
                "MERCHANT_KEY": MERCHANT_KEY,
                "txnid": txnid,
                "hash_string": hash_string,
                "action": "https://test.payu.in/_payment",
                }
        return render_to_response('orders/current_datetime.html', args)

    else:
        args = {"posted": posted, "hashh": hashh,
                "MERCHANT_KEY": MERCHANT_KEY,
                "txnid": txnid,
                "hash_string": hash_string,
                "action": action,
                }
        return render_to_response('orders/current_datetime.html', args)


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
    hashh = hashlib.sha512(retHashSeq).hexdigest().lower()
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
    return render_to_response('orders/success.html',
                              RequestContext(request, {"txnid": txnid, "status": status, "amount": amount}))


@csrf_protect
@csrf_exempt
def failure(request):
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
    salt = ""
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq).hexdigest().lower()
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
    return render_to_response("orders/Failure.html", RequestContext(request, c))
#---------------------Payments views ends--------------------------#


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


def delivery_charge(request, delivery_value):
    print("entered del")
    dv = delivery_value
    print(dv)
    #d_charge = get_object_or_404(CategoryModel, is_delivery=True)
    if dv is '1':
            print("applied")
            request.session['delivery'] = dv
            return HttpResponse(request)
    elif dv is '0':
        del request.session['delivery']
        request.session.modified = True
        return HttpResponse(request)
