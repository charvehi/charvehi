from django.db.models import Max, Min
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from time import gmtime, strftime
from django.shortcuts import render, redirect, get_object_or_404
from booking.forms import IndexBookForm
from booking.models import Category, Image, CategoryModel, CategoryModelImage
from dealer.models import Dealer
from numpy.ma import empty
from review.models import Review
from review.forms import ReviewForm
from datetime import datetime as dt
import datetime
import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from endless_pagination.decorators import page_template
# import mpu
# from Collections import defaultdict
# from django.db.models.functions import Cos, ASin
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
    # models = CategoryModel.objects.filter(status=1)
    if category_slug:
        category = get_object_or_404(Category, c_id=category_id, slug=category_slug)
        # models = CategoryModel.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
    }
    return render(request, 'booking/category/list.html', context)


def category_model_list(request):

    models = CategoryModel.objects.filter(status=1)
    loc = request.GET.get('current_loc', '')
    start = str(request.GET.get('start', ''))
    end = str(request.GET.get('end', ''))
    lat = float(request.GET.get('lat', ''))
    lon = float(request.GET.get('lon', ''))
    area = float(request.GET.get('area', ''))
    filter = str(request.GET.get('filter', ''))
    #checking format according to the url takes value
    #check = dt.strptime('1 jan 12:00 am','%d %b %I:%M %p')
    datetimeFormat1='%d %b %I:%M%p'
    check=dt.strptime(start,datetimeFormat1)
    check.strftime('%d %m %H:%M')


    #check1 = dt.strptime('2 jan 01:30 am', '%d %b %I:%M %p')
    check1=dt.strptime(end,datetimeFormat1)
    check1.strftime('%d %m %H:%M')
    newdiff = check1 \
           - check
    days, hours, minutes = newdiff.days, newdiff.seconds // 3600, newdiff.seconds % 3600 / 60.0
    print(days,hours,minutes)
    '''
    datetimeFormat = '%m-%d %I:%M %p'
    end_time=dt.strptime(end, datetimeFormat)
    end_time.strftime("%H:%M")
    start_time=dt.strptime(start, datetimeFormat)
    start_time.strftime("%H:%M")
    diff = end_time \
           - start_time
    days, hours, minutes = diff.days, diff.seconds // 3600, diff.seconds % 3600 / 60.0
    print(days,hours,minutes)
    print("Difference:", diff)
    print("Days:", diff.days)

    print("Microseconds:", diff.microseconds)
    print("Seconds:", diff.seconds)

    
     diff = end - start

    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    print
    hours, minutes, second'''
    r = 6371
    maxLat = lat + math.degrees(area / r)
    minLat = lat - math.degrees(area / r)
    maxLon = lon + math.degrees(math.asin(area / r) / math.cos(math.radians(lat)))
    minLon = lon - math.degrees(math.asin(area / r) / math.cos(math.radians(lat)))
    if models:
        dealers = Dealer.objects.filter(dealer_lat__range=(minLat, maxLat),status=True,dealer_lon__range=(minLon, maxLon))
        dealers_li = list(dealers)
        print(dealers_li)
        models_li = []
        models_list = []
        for dl in dealers_li:
            min=CategoryModel.objects.all().filter(d_id=dl).aggregate(Min('price'))
            max=CategoryModel.objects.all().filter(d_id=dl).aggregate(Max('price'))
            if filter == 'All':
                min_price = min['price__min']
                max_price = max['price__max']
            if filter == 'less_price':
                min_price = min['price__min']
                max_price = 200

            if filter == 'medium_price':
                min_price = 200
                max_price = 500

            #print(min,max)
            if filter is not None and filter != '':
                models = CategoryModel.objects.all().filter(price__range=(min_price, max_price),d_id=dl,status=1).order_by('price')
            else:
                models = CategoryModel.objects.all().filter(d_id=dl,status=1).order_by('price')
            print(models)
            models_li.append(models)

        for model in models_li:
            for m in model:
                models_list.append(m)
        print("models are")
        print(models_list)

        page = request.GET.get('page')
        paginator = Paginator(models_list, 4)
        try:
            m_li = paginator.get_page(page)
        except PageNotAnInteger:
            m_li = paginator.get_page(1)
        except EmptyPage:
            m_li = paginator.get_page(paginator.num_pages)

        context = {
            'models': m_li,
            'media_url': settings.MEDIA_URL,
            'loc': loc,
            'start': start,
            'end': end,
            'lat': lat,
            'lon': lon,
            'area': area,
            'days':days,
            'hour':hours,
            'min':minutes,

        }

        return render(request, 'booking/catmodel/model_list.html', context)


def category_model_details(request, model_id, model_slug=None):
    loc = request.GET.get('current_loc', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    lat_o = float(request.GET.get('lat', ''))
    lon_o = float(request.GET.get('lon', ''))

    lat = math.radians(float(lat_o))
    lon = math.radians(float(lon_o))
    r = 6371.0
    details = CategoryModel.objects.filter(status=1)
    if model_slug:
        details = CategoryModel.objects.filter(m_id=model_id)
        dealer = get_object_or_404(CategoryModel, m_id=model_id)
        # photo = get_object_or_404(CategoryModelImage, id=model_id)
        d_lat = math.radians(float(dealer.d_id.dealer_lat))
        d_lon = math.radians(float(dealer.d_id.dealer_lon))

        dlon = d_lon - lon
        dlat = d_lat - lat

        a = math.sin(dlat / 2) ** 2 + math.cos(lat) * math.cos(d_lat) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = r * c
        if distance < 1:
            distance *= 1000
            distance = int(distance)
            unit = 'm'
        else:
            distance = round(distance, 1)
            unit = 'km'
        print(distance)

        latest_review_list = Review.objects.filter(model=model_id).order_by('-pub_date')[:3]
        form = ReviewForm()
    context = {
        'media_url': settings.MEDIA_URL,
        'modeldetails': details,
        'form': form,
        'latest_review_list': latest_review_list,
        'loc': loc,
        'start': start,
        'end': end,
        'lat': lat_o,
        'lon': lon_o,
        'distance': distance,
        'unit': unit,
    }
    return render(request, 'booking/catmodel/model_detail.html', context)
