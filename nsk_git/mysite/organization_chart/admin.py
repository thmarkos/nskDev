from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from mysite.organization_chart.models import Chart

class CustomMPTTModelAdmin(MPTTModelAdmin):
        #specify pixel amount for this ModelAdmin only:
        mptt_level_indent = 20
admin.site.register(Chart, CustomMPTTModelAdmin)