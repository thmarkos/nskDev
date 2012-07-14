from django.conf.urls.defaults import patterns

urlpatterns = patterns('mysite.search.views',
(r'^results/$','results',{'template_name': 'search/results.html'}, 'search_results'),
(r'^search_results/$','search_results',{'template_name': 'search/search_results.html'}, 'search'),
)