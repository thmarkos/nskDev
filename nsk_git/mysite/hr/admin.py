from django.contrib import admin
from mysite.hr.models import Employee, Person, Phone, Email, WorkHistory, Education, ForeignLanguage

admin.site.register(Employee)
admin.site.register(Person)
admin.site.register(Phone)
admin.site.register(Email)
admin.site.register(WorkHistory)
admin.site.register(Education)
admin.site.register(ForeignLanguage)
