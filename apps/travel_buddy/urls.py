from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registration_page$', views.registration_page, name='registration_page'),
    url(r'^login_page$', views.login_page, name='login_page'),
    url(r'^travels$', views.travels, name='travels'),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination, name='destination'),
    url(r'^travels/add$', views.add, name='add'),
    url(r'^create$', views.create, name='create'),
    url(r'^join/(?P<id>\d+)$', views.join, name='join')
]
