from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.sign_in, name='sign_in'),
    url(r'^signout/$', views.sign_out, name='sign_out'),
]
