from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^@(?P<author_slug>[\w-]+)/$', views.show_profile, name='show_profile'),
    url(r'^@(?P<author_slug>[\w-]+)/update/$', views.update_profile, name='update_profile'),
]
