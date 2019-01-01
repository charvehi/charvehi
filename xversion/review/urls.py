from django.conf.urls import url
from . import views

app_name = 'review'

urlpatterns = [
    url(r'^$', views.review_list, name='review_list'),
    url(r'^comment/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    #url(r'^model/add_review/$', views.add_review, name='add_review'),
    url(r'^model/(?P<model_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^model/(?P<model_id>[0-9]+)/delete_review/(?P<comment_id>[0-9]+)/$', views.del_review, name='delete_review'),
    url(r'^model/edit_review/(?P<comment_id>[0-9]+)/$', views.edit_review, name='edit_review'),
]