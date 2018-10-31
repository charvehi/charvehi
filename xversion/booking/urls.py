from django.conf.urls import url
from . import views
import uaccounts.views as acc
# SET THE NAMESPACE!
app_name = 'booking'
#app_name = 'uaccounts'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^ride/$', views.index, name='index'),
    url(r'^category/$', views.category_list, name='sort_by_category'),
    #url(r'^signup/$', acc.register, name='register'),
    #url(r'^make/$', book.index, name='index'),
]

#(?P<category_slug>[-\w]+)