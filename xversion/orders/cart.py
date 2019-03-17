from decimal import Decimal
from django.conf import settings
from booking.models import CategoryModel
from booking.views import duration_calc, price_calc
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from voucher.models import Coupon


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        self.cc_cookie = None
        self.dv_cookie = None
        if 'coupon' in request.session:
            self.cc_cookie = request.session['coupon']
        #if 'delivery' in request.session:
         #   self.dv_cookie = request.session['delivery']
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, request, model, quantity=1, update_quantity=False):
        model_id = str(model.m_id)
        start = request.GET.get('start', '')
        end = request.GET.get('end', '')
        days, hours, minutes, net_hours = duration_calc(request, start, end)
        details = CategoryModel.objects.filter(m_id=model_id)
        for model in details:
            # --------------------Price calculation begins-----------------------#
            price, price_discount = price_calc(request, model, days, hours, minutes, net_hours)
            #profit_margin(request, m, days, hours, net_hours)
            model.price = price
            #model.net_price = model.price + ((model.price * 18) / 100)
            model.price_discount = price_discount
            # --------------------Price calculation ends-----------------------#

        if model_id not in self.cart:
            self.cart[model_id] = {'quantity': 0, 'price': str(model.price), 'delivery': 0}
            self.cart[model_id]['quantity'] += quantity
            #self.cart[model_id]['quantity'] += quantity
        self.save()

    def add_delivery(self, model):
        model_id = str(model.m_id)
        if model_id in self.cart:
            self.cart[model_id]['delivery'] = 1
            self.save()

    def remove_delivery(self, model):
        model_id = str(model.m_id)
        if model_id in self.cart:
            self.cart[model_id]['delivery'] = 0
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, model):
        model_id = str(model.m_id)
        if model_id in self.cart:
            del self.cart[model_id]
            self.save()

    def __iter__(self):
        model_ids = self.cart.keys()
        models = CategoryModel.objects.filter(m_id__in=model_ids)

        cart = self.cart.copy()
        for model in models:
            self.cart[str(model.m_id)]['model'] = model
            print(self.cart)

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            #item['quantity'] = 1
            item['net_price'] = Decimal(item['price']) + ((Decimal(item['price']) * 1) / 100)
            item['total_price'] = item['net_price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_sub_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        if self.cc_cookie is not None:
            cc = self.cc_cookie
            coupon = get_object_or_404(Coupon, coupon_name=cc, status=1)
            discount = coupon.discount
            print(discount)
            return sum((Decimal(item['net_price']) * item['quantity']) - (((Decimal(item['net_price']) * item['quantity']) * discount) / 100) for item in self.cart.values())
        else:
            return sum(Decimal(item['net_price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
