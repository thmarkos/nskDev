from django.conf.urls.defaults import patterns

urlpatterns = patterns('mysite.test.views',
    (r'^test/$', 'test', {'template_name': 'test/test.html'}, 'test'),
    (r'^testin/$', 'testin', {'template_name': 'test/testin.html'}, 'testin'),
    (r'^testout/$', 'testout', {}, 'testout'),
    (r'^testoutf/$', 'testoutf', {}, 'testoutf'),
)
