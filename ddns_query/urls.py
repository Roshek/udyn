from django.conf.urls import url, include
from django.views.generic import TemplateView
from registration.backends.simple.views import RegistrationView
from . import views
from .forms import CustomRegistrationForm
from django.contrib.auth import views as auth_views

app_name = 'ddns_query'
urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name="ddns_query/index.html"),
        name="index"),
    url(
        r'^accounts/register/$',
        RegistrationView.as_view(
            form_class=CustomRegistrationForm
        ),
        name='registration_register'
    ),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^login/$',
        auth_views.login,
        name='login'),
    url(r'^logout/$',
        auth_views.logout,
        name='logout'),

    url(r'^get/(?P<host_name>[a-z,0-9]{1,15})/$',
        views.get_address, name='get_ip'),
    url(
        r'^add/$',
        views.addDyname,
        name='add'
    ),
    url(
        r'^update/$',
        views.updateDyname,
        name='update'
    ),
    url(
        r'^mydomains/$',
        TemplateView.as_view(template_name="ddns_query/mydomains.html"),
        name="mydomains"
    )
    # url(r'^set/(?P<host_name>[a-z,0-9]{1,15})/$',
    #    views.set_hostname, name='set_hostname'),
]
