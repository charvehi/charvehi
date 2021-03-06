"""xversion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include

from booking import views as book
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from UserAccounts.forms import NewPasswordResetForm
from django.contrib.auth.views import (LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView)
from orders import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('mylocation/maps/', TemplateView.as_view(template_name='booking/aindex/map.html'), name='maps'),
    #path('booking/', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^admin/orders/report/$', views.order_report, name='order_report'),
    url(r'^$', book.index, name='index'),
    url(r'^dealer/', include('dealer.urls', namespace='dealer')),#url for dealr rr
    url(r'^accounts/', include('UserAccounts.urls', namespace='useraccounts')),#replace uaccounts later above url
    url(r'^bike/', include('booking.urls'), name='category'),
    url(r'^bike/book/', include('orders.urls'), name='orders'),
    url(r'^coupon/', include('voucher.urls'), name='voucher'),
    url(r'^bike/reviews/', include('review.urls', namespace="review")),

    url(r'^password_reset/$', PasswordResetView.as_view(form_class=NewPasswordResetForm, template_name='registration/password_reset_form.html'), name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html') , name='password_reset_complete'),

##################################index page urls###################################
path('about-us/', TemplateView.as_view(template_name='booking/aindex/about_us.html'), name='about-us'),
path('contact-us/', TemplateView.as_view(template_name='booking/aindex/contactus.html'), name='contact-us'),
path('pricing-and-delivery/', TemplateView.as_view(template_name='booking/aindex/pricing_n_delivery.html'), name='pricing-delivery'),
path('privacy-policy/', TemplateView.as_view(template_name='booking/aindex/privacy_policy.html'), name='privacy-policy'),
path('refund-rules/', TemplateView.as_view(template_name='booking/aindex/refund_n_cancel.html'), name='refund-rules'),
path('terms-and-conditions/', TemplateView.as_view(template_name='booking/aindex/tnc.html'), name='terms-conditions'),
##################################index page urls ends###################################


    #path('', include('booking.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
