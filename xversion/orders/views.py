from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from booking.models import CategoryModel
from .cart import Cart
from .forms import CartAddProductForm


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
                    quantity=item['quantity']
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
        cart.add(model=model, quantity=1)
    return redirect('orders:cart_detail')
    #return render(request, 'orders/order_list.html', {'cart': cart})

def cart_remove(request, model_id):
    cart = Cart(request)
    product = get_object_or_404(CategoryModel, m_id=model_id)
    cart.remove(product)
    return redirect('orders:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    #for item in cart:
     #   item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    context = {
        'media_url': settings.MEDIA_URL,
        'cart': cart,
    }
    return render(request, 'orders/order_list.html', context)
