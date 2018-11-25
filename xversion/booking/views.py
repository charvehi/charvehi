from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from time import gmtime, strftime
from django.shortcuts import render, get_object_or_404
from booking.forms import IndexBookForm
from booking.models import Category, Image, CategoryModel, CategoryModelImage
from dealer.models import Dealer


def index(request):
    index_form = IndexBookForm(request.POST or None)
    if index_form.is_valid():
        index_form.save()

    context = {'form': index_form}
    return render(request, 'booking/aindex/index.html', context)


def location(request):
    return render(request, 'booking/aindex/map.html')


def datetime(request):
    if request.method == 'POST':
        if request.POST.get("now"):
            return strftime("%Y-%m-%d %H:%M:%S", gmtime())
        elif request.POST.get("schedule"):
            return HttpResponseRedirect(reverse('portal_sec2'))


def index_book_form(request):
    index_form = IndexBookForm(request.POST or None)
    if index_form.is_valid():
        index_form.save()

    context = {'form': index_form}
    return render(request, 'booking/aindex/index.html', context)

'''def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    return render(request, 'shop/product/detail.html', context)'''


def category_list(request, category_id=None, category_slug=None):
    category = None
    categories = Category.objects.all()
    #models = CategoryModel.objects.filter(status=1)
    if category_slug:
        category = get_object_or_404(Category, c_id=category_id, slug=category_slug)
        #models = CategoryModel.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
    }
    return render(request, 'booking/category/list.html', context)


def category_model_list(request, category_id, category_slug=None):
    models = CategoryModel.objects.filter(status=1)
    if category_slug:
        category = get_object_or_404(Category, c_id=category_id, status=1)
        dealers = get_object_or_404(Dealer, dealer_lat=79, dealer_lon=26)
        models = CategoryModel.objects.filter(c_id=category, d_id=dealers)

    context = {
        'models': models,
    }
    return render(request, 'booking/catmodel/model_list.html', context)


def category_model_details(request, model_id, model_slug=None):
    details = CategoryModel.objects.filter(status=1)
    if model_slug:
        details = CategoryModel.objects.filter(m_id=model_id)

    context = {
        'modeldetails': details,
    }
    return render(request, 'booking/catmodel/model_detail.html', context)
