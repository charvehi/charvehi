from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from time import gmtime, strftime
from django.shortcuts import render, get_object_or_404
from booking.forms import IndexBookForm
from booking.models import Category, Image, CategoryModel, CategoryModelImage
from dealer.models import Dealer
import math
#from Collections import defaultdict
#from django.db.models.functions import Cos, ASin
from decimal import Decimal


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
        print("Form is valid")
        
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


def category_model_details(request, model_id, model_slug=None):
    details = CategoryModel.objects.filter(status=1)
    if model_slug:
        details = CategoryModel.objects.filter(m_id=model_id)

    context = {
        'modeldetails': details,
    }
    return render(request, 'booking/catmodel/model_detail.html', context)


def category_model_list(request, category_id, category_slug=None):
    models = CategoryModel.objects.filter(status=1)
    lat = float(request.GET.get('lat', ''))
    lon = float(request.GET.get('lon', ''))
    area = float(request.GET.get('area', ''))
    r = 6371
    maxLat = lat + math.degrees(area / r)
    minLat = lat - math.degrees(area / r)
    maxLon = lon + math.degrees(math.asin(area / r) / math.cos(math.radians(lat)))
    minLon = lon - math.degrees(math.asin(area / r) / math.cos(math.radians(lat)))
    if category_slug:
        category = get_object_or_404(Category, c_id=category_id, status=1)
        #dealers = get_object_or_404(Dealer, dealer_lat__range=(minLat, maxLat), dealer_lon__range=(minLon, maxLon))
        dealers = Dealer.objects.filter(dealer_lat__range=(minLat, maxLat), dealer_lon__range=(minLon, maxLon))
        dealers_li = list(dealers)
        print(dealers_li)
        models_li = []

        for dl in dealers_li:
            models = CategoryModel.objects.all().filter(c_id=category, d_id=dl)
            print(models)
            models_li.append(models)

        print("models are")
        print(models_li)

        context = {
            'models': models_li,
        }
        print(context)
        #return render_to_response('booking/catmodel/model_list.html', context, context_instance=RequestContext(request))
        return render(request, 'booking/catmodel/model_list.html', context)



