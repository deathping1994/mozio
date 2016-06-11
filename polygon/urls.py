from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^test/$', views.test),
    url(r'^(?P<id>[0-9a-f]{24})/area/$', views.update_service_area),
    url(r'^(?P<id>[0-9a-f]{24})/$', views.service_provider, name='service_provider'),
    url(r'^all/$', views.service_provider, name='service_provider'),
    url(r'', views.service_provider, name='service_provider'),
]
