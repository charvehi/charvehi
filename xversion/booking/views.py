# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from time import gmtime, strftime
from django.shortcuts import render, get_object_or_404
from booking.models import Category, Image
#from cart.forms import CartAddProductForm

def index(request):
    return render(request,'booking/index.html')

def datetime(request):
    if request.method == 'POST':
        if request.POST.get("now"):
            return strftime("%Y-%m-%d %H:%M:%S", gmtime())
        elif request.POST.get("schedule"):
            return HttpResponseRedirect(reverse('portal_sec2'))


def category_list(request, category_slug=None):
    #category = None
    #categories = Category.objects.all()
    category = Category.objects.filter(status=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        category = Category.objects.filter(category=category)

    context = {
        'category': category,
        #'categories': categories,
        #'products': products
    }
    return render(request, 'booking/category/list.html', context)


'''def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    return render(request, 'shop/product/detail.html', context)'''