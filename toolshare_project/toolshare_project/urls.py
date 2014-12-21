from django.conf.urls import patterns, include, url
from django.contrib import admin
from toolshare_project import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^account/', include('users.urls')),
	url(r'^tools/', include('tools.urls')),
	url(r'^toolsheds/', include('toolsheds.urls')),
	url(r'^communities/', include('communities.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.index, name='index'),
)
