from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^log/$', views.log, name='log'),
    url(r'^sign/$', views.sign, name='sign'),
    url(r'^blog/$', views.blog, name='blog'),
    url(r'$', views.home, name='home'),
]
