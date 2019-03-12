from django.conf.urls import url
from . import views
from . import cart
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from orders.views import Home, success, failure

app_name = 'orders'

urlpatterns = [
    #url(r'^make_purchase/(?P<model_id>\d+)/(?P<model_slug>[-\w]+)/$', views.order_details, name='user_cart'),
    url(r'^net_amount/$', cart.Cart.get_total_price, name='total_price'),
    url(r'^orders/$', views.cart_detail, name='cart_detail'),
    url(r'^make_purchase/add/(?P<model_id>\d+)/(?P<model_slug>[-\w]+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<model_id>\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^delivery/apply/(?P<delivery_value>[-\w]+)/$', views.delivery_charge, name='delivery_charge'),
    #-----------------------Payments urls begin----------------------------#
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^redirect_to_payment/', Home),
    url(r'^success/', success),
    url(r'^failure/', failure),
    # -----------------------Payments urls ends----------------------------#
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

