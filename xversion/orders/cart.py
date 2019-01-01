from decimal import Decimal
from django.conf import settings
from booking.models import CategoryModel
from django.http import JsonResponse


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, model, quantity=1, update_quantity=False):
        model_id = str(model.m_id)
        if model_id not in self.cart:
            self.cart[model_id] = {'quantity': 0, 'price': str(model.price)}
            self.cart[model_id]['quantity'] += quantity
            #self.cart[model_id]['quantity'] += quantity
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
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
