from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^log/$', views.log, name='log'),
    url(r'^sign/$', views.sign, name='sign'),
    url(r'^blog/([0-9]+)/$', views.blog, name='blog'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^hadmin/$', views.admin, name='admin'),
    url(r'^$', views.home, name='home'),
]
