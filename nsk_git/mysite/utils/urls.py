from django.conf.urls.defaults import patterns

urlpatterns = patterns('mysite.utils.views',
	(r'^genres/$', 'show_genres', {'template_name': 'utils/genres.html'}, 'genres'),
)
