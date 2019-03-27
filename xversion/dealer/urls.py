from django.conf.urls import url
from django.urls import path

from . import views
app_name = 'dealer'
urlpatterns =[
    url(r'^detailshow/$',views.show,name='show'),
    url(r'^happyrides/$', views.rides, name='rides'),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
]
