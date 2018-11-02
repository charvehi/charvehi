from django.conf.urls import url
from . import views
import uaccounts.views as acc
# SET THE NAMESPACE!
app_name = 'booking'
#app_name = 'uaccounts'

# Be careful setting the name to just /login use userlogin instead

urlpatterns = [
    url(r'^ride/$', views.index, name='index'),
    url(r'^$', views.model_list, name='model_list'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.model_list, name='model_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.CategoryModel_detail, name='CategoryModel_detail'),
]