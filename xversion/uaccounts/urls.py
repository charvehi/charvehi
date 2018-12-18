from django.conf.urls import url
from . import views
from booking import views as book

# SET THE NAMESPACE!
app_name = 'uaccounts'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^signup/$',views.register, name='register'),
    url(r'^home/$',views.index, name='index'),
    url(r'^signin/$',views.user_login, name='user_login'),
    url(r'^logout/$',views.user_logout, name='user_logout'),
    #url(r'^signout/$', views.user_login, name='user_logout'),
    url(r'^$', views.index, name='index'),
    #url(r'^home/$', book.index, name='index'),
]