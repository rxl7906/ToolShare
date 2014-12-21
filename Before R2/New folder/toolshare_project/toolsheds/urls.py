from django.conf.urls import patterns, url
from toolsheds import views

urlpatterns = patterns('',
	url(r'^my_toolshed/$', views.my_toolshed, name='my_toolshed'),
	url(r'^community_toolshed/$', views.community_toolshed, name='community_toolshed'),
)