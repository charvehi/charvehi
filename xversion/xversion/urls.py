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
from uaccounts import views as acc
from booking import views as book
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('booking/', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^$', book.index, name='index'),
    url(r'^$', acc.index, name='index'),
    url(r'^special/', acc.special,name='special'),
    url(r'^uaccounts/', include('uaccounts.urls')),
    url(r'^bike/', include('booking.urls')),
    url(r'^signout/$', acc.user_logout, name='logout'),
    #path('', include('booking.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)