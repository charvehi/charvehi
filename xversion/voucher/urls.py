from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'voucher'

urlpatterns = [
    url(r'^apply/(?P<coupon_name>[-\w]+)/$', views.cart_coupon, name='cart_coupon'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
