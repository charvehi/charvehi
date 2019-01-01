from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'orders'

urlpatterns = [
    #url(r'^make_purchase/(?P<model_id>\d+)/(?P<model_slug>[-\w]+)/$', views.order_details, name='user_cart'),
    url(r'^orders/$', views.cart_detail, name='cart_detail'),
    url(r'^make_purchase/add/(?P<model_id>\d+)/(?P<model_slug>[-\w]+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<model_id>\d+)/$', views.cart_remove, name='cart_remove'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
