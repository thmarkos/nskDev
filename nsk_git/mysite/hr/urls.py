from django.conf.urls.defaults import patterns

urlpatterns = patterns('mysite.hr.views',
    (r'^home/$', 'home', {'template_name': 'index.html'}, 'home'),
    
    (r'^employee/detail/(?P<employee_slug>\d+)/$', 'employee_detail', {'template_name': 'hr/employee_detail.html'}, 'employee_detail'),
    (r'^employee/add/$', 'employee_form_add', {'template_name': 'hr/employee_form_core.html'}, 'employee_form_add'),
    (r'^employee/update_core/(?P<employee_id>\d+)/$', 'employee_form_update_core', {'template_name': 'hr/employee_form_core.html'}, 'employee_form_update_core'),
    (r'^employee/update_extra/(?P<employee_id>\d+)/$', 'employee_form_update_extra', {'template_name': 'hr/employee_form_extra.html'}, 'employee_form_update_extra'),
    (r'^employee/list/$', 'employee_list', {'template_name': 'hr/employee_list.html'}, 'employee_list'),
    (r'^employee/list/(?P<employee_code>\d+)/$', 'employee_chart_list', {'template_name': 'hr/employee_chart_list.html'}, 'employee_list_filter'),
    (r'^employee/delete/(?P<employee_id>\d+)/$', 'employee_delete', {}, 'employee_delete'),
    
    (r'^person/add/(?P<employee_id>\d+)/$', 'person_form_add', {'template_name': 'hr/person_form.html'}, 'person_form_add'),
    (r'^person/update/(?P<employee_id>\d+)/(?P<person_id>\d+)/$', 'person_form_update', {'template_name': 'hr/person_form.html'}, 'person_form_update'),
    (r'^person/update/(?P<employee_id>\d+)/$', 'person_formset_update', {'template_name': 'hr/person_formset.html'}, 'person_formset_update'),
    (r'^person/delete/(?P<employee_id>\d+)/(?P<person_id>\d+)/$', 'person_delete', {}, 'person_delete'),
    
    (r'^phone/add/(?P<employee_id>\d+)/(?P<phone_type>[WPE])/$', 'phone_form_add', {'template_name': 'hr/phone_form.html'}, 'phone_form_add'),    
    (r'^phone/update/(?P<employee_id>\d+)/(?P<phone_id>\d+)/$', 'phone_form_update', {'template_name': 'hr/phone_form.html'}, 'phone_form_update'),
    (r'^phone/update/(?P<employee_id>\d+)/(?P<phone_type>[WPE])/$', 'phone_formset_update', {'template_name': 'hr/phone_formset.html'}, 'phone_formset_update'),
    (r'^phone/delete/(?P<employee_id>\d+)/(?P<phone_id>\d+)/$', 'phone_delete', {}, 'phone_delete'),
    
    (r'^email/add/(?P<employee_id>\d+)/(?P<email_type>[WP])/$', 'email_form_add', {'template_name': 'hr/email_form.html'}, 'email_form_add'),    
    (r'^email/update/(?P<employee_id>\d+)/(?P<email_id>\d+)/$', 'email_form_update', {'template_name': 'hr/email_form.html'}, 'email_form_update'),
    (r'^email/update/(?P<employee_id>\d+)/(?P<email_type>[WP])/$', 'email_formset_update', {'template_name': 'hr/email_formset.html'}, 'email_formset_update'),
    (r'^email/delete/(?P<employee_id>\d+)/(?P<email_id>\d+)/$', 'email_delete', {}, 'email_delete'),
    
    (r'^work_history/add/(?P<employee_id>\d+)/$', 'workhistory_form_add', {'template_name': 'hr/workhistory_form.html'}, 'workhistory_form_add'),    
    (r'^work_history/update/(?P<employee_id>\d+)/(?P<work_history_id>\d+)/$', 'workhistory_form_update', {'template_name': 'hr/workhistory_form.html'}, 'workhistory_form_update'),
    (r'^work_history/delete/(?P<employee_id>\d+)/(?P<work_history_id>\d+)/$', 'workhistory_delete', {}, 'workhistory_delete'),

    (r'^education/add/(?P<employee_id>\d+)/$', 'education_form_add', {'template_name': 'hr/education_form.html'}, 'education_form_add'),    
    (r'^education/update/(?P<employee_id>\d+)/(?P<education_id>\d+)/$', 'education_form_update', {'template_name': 'hr/education_form.html'}, 'education_form_update'),
    (r'^education/delete/(?P<employee_id>\d+)/(?P<education_id>\d+)/$', 'education_delete', {}, 'education_delete'),
    
    (r'^foreign_language/add/(?P<employee_id>\d+)/$', 'foreign_language_form_add', {'template_name': 'hr/foreign_language_form.html'}, 'foreign_language_form_add'),    
    (r'^foreign_language/update/(?P<employee_id>\d+)/(?P<foreign_language_id>\d+)/$', 'foreign_language_form_update', {'template_name': 'hr/foreign_language_form.html'}, 'foreign_language_form_update'),
    (r'^foreign_language/delete/(?P<employee_id>\d+)/(?P<foreign_language_id>\d+)/$', 'foreign_language_delete', {}, 'foreign_language_delete'),
)