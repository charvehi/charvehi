from django.contrib import admin
from booking.models import Category, Image, CategoryModel, CategoryModelImage


admin.site.register(Category)
admin.site.register(Image)
admin.site.register(CategoryModelImage)
admin.site.register(CategoryModel)
