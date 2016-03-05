from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^@(?P<author_slug>[\w-]+)/story/create/$', views.create_story, name='create_story'),
    url(r'^@(?P<author_slug>[\w-]+)/(?P<story_slug>[\w-]+)/edit/$', views.edit_story, name='edit_story'),
    url(r'^@(?P<author_slug>[\w-]+)/(?P<story_slug>[\w-]+)/$', views.story, name='story'),
    url(r'^@(?P<author_slug>[\w-]+)/(?P<story_slug>[\w-]+)/chapter/create$', views.create_chapter, name='create_chapter'),
    url(r'^@(?P<author_slug>[\w-]+)/(?P<story_slug>[\w-]+)/(?P<chapter_slug>[\w-]+)/edit$', views.edit_chapter, name='edit_chapter'),
    url(r'^@(?P<author_slug>[\w-]+)/(?P<story_slug>[\w-]+)/(?P<chapter_slug>[\w-]+)/$', views.chapter, name='chapter'),
    url(r'^home/$', views.home, name="home"),
    url(r'^topstories/$', views.top_stories, name="top_stories"),

]
