from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get/(?P<host_name>[a-z,0-9]{1,15})/$',
        views.get_address, name='get_ip'),
    url(r'^set/(?P<host_name>[a-z,0-9]{1,15})/$',
        views.set_hostname, name='set_hostname'),
]
