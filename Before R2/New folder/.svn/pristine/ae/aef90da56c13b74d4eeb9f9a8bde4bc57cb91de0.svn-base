from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
	url(r'^$', views.profile, name='profile'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^join_community/$', views.join_community, name='join_community'),
	url(r'^signin/$', views.signin, name='signin'),
	url(r'^signout/$', views.signout, name='signout'),
	url(r'^send_message/$', views.send_message, name='send_message'),
	url(r'^messages/$', views.messages, name='messages'),
	url(r'^change_password/$', views.change_password, name='change_password'),
	url(r'^change_name/$', views.change_name, name='change_name'),
	url(r'^change_zip_code/$', views.change_zip_code, name='change_zip_code'),
	url(r'^change_pickup_arrangement/$', views.change_pickup_arrangement, name='change_pickup_arrangement'),
	url(r'^delete_account/$', views.delete_account, name='delete_account')
           
)
