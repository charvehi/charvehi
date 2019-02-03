from django.contrib import admin
from booking.models import Category, Image, CategoryModel, CategoryModelImage



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}

class ModelAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug':('model_name',)}
admin.site.register(Category, CategoryAdmin)

admin.site.register(Image)
admin.site.register(CategoryModelImage)
admin.site.register(CategoryModel,ModelAdmin)
