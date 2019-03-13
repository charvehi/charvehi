from django.db.models import Max, Min
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.conf import settings
from time import gmtime, strftime
from django.shortcuts import render, get_object_or_404
from booking.forms import IndexBookForm
from django.contrib.auth import get_user_model
from booking.models import Category, Image, CategoryModel, CategoryModelImage
from dealer.models import Dealer
from review.models import Review
from review.forms import ReviewForm
from datetime import datetime as dt
import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()


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


def category_list(request, category_id=None, category_slug=None):
    category = None
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, c_id=category_id, slug=category_slug)

    context = {
        'category': category,
        'categories': categories,
    }
    return render(request, 'booking/category/list.html', context)

def profit_margin(request, models, days, hours, net_hours):
    priceHourD = models.price_hour_dealer
    priceDayD = models.price_day_dealer
    priceHour = models.price_hour
    PH_Count = models.ph_count
    priceDay = models.price_day
    PD_count = models.pd_count

    if days is 0 or hours <= PH_Count:        #hourly charges
        price = priceHour*hours
        priceD = priceHourD*hours
    if days is not 0 and hours > PH_Count:        #day charges
        price = (float(priceDay)*(net_hours/PD_count))+(float(priceHour)
                                                                     * (net_hours % PD_count))
        priceD = (float(priceDayD)*(net_hours/PD_count))+(float(priceHourD)
                                                                     * (net_hours % PD_count))
    gross_profit = price-priceD
    profit_cent = (gross_profit/price)*100
    print("Profit margin:", gross_profit)
    print("Profit percentage:", profit_cent)
    return 0


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


def price_calc(request, models, days, hours, minutes, net_hours):
    priceHourOff = models.price_hour_offline
    priceDayOff = models.price_day_offline
    priceHour = models.price_hour
    PH_Count = models.ph_count
    priceDay = models.price_day
    PD_count = models.pd_count

    min_factor = 0
    if int(minutes) is not 0:
        min_factor = 1

    if PD_count is 1:
        PD_count = 12
    else:
        PD_count = 24

    if PD_count >= net_hours > PH_Count:
        price = (float(priceDay))
        priceOff = (float(priceDayOff))

    elif net_hours >= PD_count:
        price = ((float(priceDay)) * (int(net_hours / PD_count))) + (float(priceHour) * \
                int(net_hours % PD_count)) + ((float(priceHour) / 2) * min_factor)
        priceOff = ((float(priceDayOff)) * (int(net_hours / PD_count))) + (float(priceHourOff) * \
                   int(net_hours % PD_count)) + ((float(priceHourOff) / 2) * min_factor)
    elif net_hours < PD_count:
        price = int(net_hours) * float(priceHour) + ((float(priceHour) / 2) * min_factor)
        priceOff = int(net_hours) * float(priceHourOff) + ((float(priceHour) / 2) * min_factor)
    print(int(net_hours % PD_count))
    print(PD_count)
    price_discount = priceOff - price
    return price, price_discount


def category_model_list(request):

    if 'current_loc' not in request.GET or 'start' not in request.GET or 'end' not in request.GET or \
            'lat' not in request.GET or 'lon' not in request.GET or \
            'area' not in request.GET:
        return HttpResponseBadRequest("Something went wrong")
    elif request.GET.get('current_loc', '') == '' or request.GET.get('start', '') == ''\
            or request.GET.get('end', '') == '' or request.GET.get('lat', '') == ''\
            or request.GET.get('lon', '') == '' or request.GET.get('area', '') == '':
        return HttpResponseBadRequest("Something went wrong")

    models = CategoryModel.objects.filter(status=1)
    loc = request.GET.get('current_loc', '')
    start = str(request.GET.get('start', ''))
    end = str(request.GET.get('end', ''))
    lat = float(request.GET.get('lat', ''))
    lon = float(request.GET.get('lon', ''))
    area = float(request.GET.get('area', ''))
    filter_price = str(request.GET.get('filter', ''))

    days, hours, minutes, net_hours = duration_calc(request, start, end)

    r = 6371
    maxLat = lat + math.degrees(area / r)
    minLat = lat - math.degrees(area / r)
    maxLon = lon + math.degrees(math.asin(area / r) / math.cos(math.radians(lat)))
    minLon = lon - math.degrees(math.asin(area / r) / math.cos(math.radians(lat)))
    if models:
        dealers = Dealer.objects.filter(dealer_lat__range=(minLat, maxLat), dealer_lon__range=(minLon, maxLon))
        dealers_li = list(dealers)
        print(dealers_li)
        models_li = []
        models_list = []
        for dl in dealers_li:
            minPrice = CategoryModel.objects.all().filter(d_id=dl).aggregate(Min('price_hour'))
            maxPrice = CategoryModel.objects.all().filter(d_id=dl).aggregate(Max('price_hour'))
            if filter_price == 'All':
                min_price = minPrice['price_hour__min']
                max_price = maxPrice['price_hour__max']

            if filter_price == 'less_price':
                min_price = minPrice['price_hour__min']
                max_price = 56

            if filter_price == 'medium_price':
                min_price = 50
                max_price = 100

            if filter_price == 'high_price':
                min_price = 90
                max_price = 200

            if filter_price is not None and filter_price != '':
                models = CategoryModel.objects.all().filter(price_hour__range=(min_price, max_price), d_id=dl, status=1).\
                    order_by('price_hour')
            else:
                models = CategoryModel.objects.all().filter(d_id=dl, status=1).order_by('price_hour')
            print(models)
            models_li.append(models)

        for model in models_li:
            for m in model:
                # --------------------Price calculation begins-----------------------#
                price, price_discount = price_calc(request, m, days, hours, minutes, net_hours)
                m.price = price
                m.price_discount = price_discount
                # --------------------Price calculation ends-----------------------#
                models_list.append(m)

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
            'days': days,
            'hour': hours,
            'min': minutes,
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
    if model_slug is not None:
        details = CategoryModel.objects.filter(m_id=model_id)
        dealer = get_object_or_404(CategoryModel, m_id=model_id)

        days, hours, minutes, net_hours = duration_calc(request, start, end)

        for m in details:
            # --------------------Price calculation begins-----------------------#
            m.price, m.price_discount = price_calc(request, m, days, hours, minutes, net_hours)
            # --------------------Price calculation ends-----------------------#
            # --------------------Model suggestion begins-----------------------#
            model_suggestions = CategoryModel.objects.filter(d_id=m.d_id.d_id).exclude(m_id=m.m_id)
            review_exist = Review.objects.filter(user_id=request.user.id, model=m.m_id)
            # --------------------Model suggestion ends-----------------------#


        #-----------------------Location script--------------------------#
        d_lat = math.radians(float(dealer.d_id.dealer_lat))
        d_lon = math.radians(float(dealer.d_id.dealer_lon))

        dlon = d_lon - lon
        dlat = d_lat - lat

        a = math.sin(dlat / 2) ** 2 + math.cos(lat) * math.cos(d_lat) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = r * c
        if distance < 1:
            distance *= 1000
            distance = str(int(distance))+'m'
        else:
            distance = str(round(distance, 1))+'km'
        #------------------------Location script ends-----------------------#

        latest_review_list = Review.objects.filter(model=model_id).order_by('-pub_date')[:3]

        review = False
        uid = None
        if review_exist.exists():
            review = True
        if request.user.is_authenticated:
            uid = request.user.id
        form = ReviewForm()
    context = {
        'media_url': settings.MEDIA_URL,
        'user_id': uid,
        'modeldetails': details,
        'form': form,
        'modelsuggest': model_suggestions,
        'latest_review_list': latest_review_list,
        'review_bit': review,
        'loc': loc,
        'start': start,
        'end': end,
        'lat': lat_o,
        'lon': lon_o,
        'distance': distance,
    }
    return render(request, 'booking/catmodel/model_detail.html', context)
