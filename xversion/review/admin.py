from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('model', 'rating', 'user_id', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_id']
    search_fields = ['comment']


admin.site.register(Review, ReviewAdmin)
