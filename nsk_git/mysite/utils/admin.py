from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from mysite.utils.models import Genre

class CustomMPTTModelAdmin(MPTTModelAdmin):
		#specify pixel amount for this ModelAdmin only:
		mptt_level_indent = 20
admin.site.register(Genre, CustomMPTTModelAdmin)