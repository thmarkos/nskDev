from django.conf.urls.defaults import patterns
from mysite.accounts.forms import AuthenticationFormCustom

urlpatterns = patterns('mysite.accounts.views',
	(r'^my_account/$', 'my_account', {'template_name': 'registration/my_account.html'}, 'my_account'),
	(r'^my_account/preferences/$', 'change_preference', {}, 'change_preference'),
)
urlpatterns += patterns('django.contrib.auth.views',
	(r'^login/$', 'login', {'template_name': 'registration/login.html', 'authentication_form': AuthenticationFormCustom}, 'login'),
	(r'^logout/$', 'logout_then_login', '', 'logout'),
#	(r'^logout/$', 'logout', {'template_name': 'registration/logged_out.html'}, 'logout'),
)