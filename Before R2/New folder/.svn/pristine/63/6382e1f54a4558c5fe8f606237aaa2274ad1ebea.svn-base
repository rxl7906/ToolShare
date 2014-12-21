from django.conf.urls import patterns, url
from communities import views

urlpatterns = patterns('',
	url(r'^$', views.main, name='main'),
	url(r'^admin/$', views.admin, name='admin'),
	url(r'^rate/$', views.rate, name='rate'),
	url(r'^statistics/$', views.statistics, name='statistics'),
	url(r'^post_review/$', views.post_review, name='post_review'),
	url(r'^reviews/$', views.reviews, name='reviews'),
	url(r'^remove_tool/$', views.remove_tool, name='remove_tool'),
	url(r'^remove_user/$', views.remove_user, name='remove_user'),
)