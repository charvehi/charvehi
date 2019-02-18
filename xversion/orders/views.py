from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from orders.models import UserOrderInfo
from booking.models import CategoryModel
from .cart import Cart
import datetime
from django.contrib.auth.decorators import login_required
from .forms import CartAddProductForm


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

'''def order_details(request, model_slug = None, model_id = None):
    print("Details")
    slug = model_slug
    context = {
        'list': list
    }
    return render(request, "orders/order_list.html", context)'''


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
