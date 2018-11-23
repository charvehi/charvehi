from django.conf.urls import url
from . import views
import uaccounts.views as acc
# SET THE NAMESPACE!
app_name = 'booking'
#app_name = 'uaccounts'

# Be careful setting the name to just /login use userlogin instead

urlpatterns = [
    url(r'^ride/$', views.index, name='index'),
    url(r'^$', views.category_list, name='model_list'),
    url(r'^book/$', views.index_book_form, name='index_form'),
    url(r'^category/$', views.category_list, name='model_list'),
    url(r'^models/(?P<category_id>[-\w]+)/(?P<category_slug>[-\w]+)/$', views.category_model_list, name='model_list_by_category'),
    url(r'^details/(?P<model_id>\d+)/(?P<model_slug>[-\w]+)/$', views.category_model_details, name='category_model_details'),
    url(r'^mylocation/$', views.location, name='select_loc'),
]