from django.conf.urls.defaults import patterns

urlpatterns = patterns('mysite.organization_chart.views',
    (r'^chart/$', 'show_chart', {'template_name': 'organization_chart/chart.html'}, 'chart'),
)