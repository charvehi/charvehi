from django.conf.urls import url
from booking import views as book
import uaccounts.views as acc
# SET THE NAMESPACE!
app_name = 'booking'
#app_name = 'uaccounts'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^ride/$', book.index, name='index'),
    #url(r'^signup/$', acc.register, name='register'),
    #url(r'^make/$', book.index, name='index'),
]