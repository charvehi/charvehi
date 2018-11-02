from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from time import gmtime, strftime
from django.shortcuts import render, get_object_or_404
from booking.models import Category, Image, CategoryModel, CategoryModelImage


def index(request):
    return render(request,'booking/index.html')

def datetime(request):
    if request.method == 'POST':
        if request.POST.get("now"):
            return strftime("%Y-%m-%d %H:%M:%S", gmtime())
        elif request.POST.get("schedule"):
            return HttpResponseRedirect(reverse('portal_sec2'))


def model_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    models = CategoryModel.objects.filter(status=1)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        models = CategoryModel.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'models': models
    }
    return render(request, 'booking/category/list.html', context)


def CategoryModel_detail(request, id, slug):
    CategoryModel = get_object_or_404(CategoryModel, id=id, slug=slug, available=True)
    cart_CategoryModel_form = CartAddCategoryModelForm()
    context = {
        'CategoryModel': CategoryModel,
        'cart_CategoryModel_form': cart_CategoryModel_form
    }
    return render(request, 'shop/CategoryModel/detail.html', context)
