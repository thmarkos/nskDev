from django.conf.urls.defaults import patterns, include, url
from mysite import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^hr/', include('hr.urls')),
    
    #url(r'^mgmt/', include('mgmt.urls')),

    url(r'^utils/', include('utils.urls')),

    url(r'^search/', include('search.urls')),

    url(r'^organization_chart/', include('organization_chart.urls')),

    url(r'^reports/', include('reports.urls')),

    url(r'^test/', include('test.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
       
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
