from django.conf.urls import patterns, url
from tools import views

urlpatterns = patterns('',
	url(r'^add_tool/$', views.add_tool, name='add_tool'),
	url(r'^delete_tool/$', views.delete_tool, name='delete_tool'),
	url(r'^borrow_tool/$', views.borrow_tool, name='borrow_tool'),
	url(r'^approve_request/$', views.approve_request, name='approve_request'),
	url(r'^reject_request/$', views.reject_request, name='approve_request'),
	url(r'^return_tool/$', views.return_tool, name='return_tool'),
	url(r'^make_available/$', views.make_available, name='make_available'),
	url(r'^make_unavailable/$', views.make_unavailable, name='make_unavailable'),
)
