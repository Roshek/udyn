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

    url(
        r'^add/$',
        views.addDyname,
        name='add'
    ),
    url(
        r'^modify/(?P<prefix>[a-zA-Z0-9]+)/$',
        views.modifyDyname,
        name='modify_dyname'
    ),
    url(
        r'^delete/$',
        views.deleteDyname,
        name='delete_dyname'
    ),
    url(
        r'^update/$',
        views.updateDyname,
        name='update'
    ),
    url(
        r'^update/token/$',
        views.updateToken,
        name='update_token'
    ),
    url(
        r'^mydomains/$',
        TemplateView.as_view(template_name="ddns_query/mydomains.html"),
        name="mydomains"
    )
]
