from django.conf.urls.defaults import patterns

urlpatterns = patterns('mysite.reports.views',
(r'^reports/(?P<employee_id>\d+)/$','report',{}, 'report'),
)