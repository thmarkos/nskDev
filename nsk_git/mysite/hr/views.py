# -*- coding: utf-8 -*-
from django.forms.models import modelformset_factory
from mysite.hr.models import Employee, Person, Phone, Email, WorkHistory, Education, ForeignLanguage
from mysite.hr.forms import EmployeeFormCore, EmployeeFormExtra, EmployeeFormCoreUpdate, PersonForm, PhoneForm, PhoneFormEmergency, EmailForm, WorkHistoryForm, WorkHistoryFormUpdate, EducationForm, ForeignLanguageForm, DivErrorList
from mysite.organization_chart.models import Chart
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from mysite import settings
#from django.core.exceptions import ObjectDoesNotExist
#from django.db.models import Max
#from django.template.defaultfilters import slugify

@login_required
def home(request, template_name="index.html"):
    title='Αρχική Σελίδα'
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.add_employee')
def employee_form_add(request, template_name="hr/employee_form_core.html"):
    title='Add Employee'
    saved=False
    if request.method == 'POST':
        form = EmployeeFormCore(request.POST, request.FILES, error_class=DivErrorList)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.created_by = request.user
            #employee.slug = slugify(form.cleaned_data['name'])
            employee.save()
            #form.save()
            saved=True
            
            if request.POST['submit']=='Υποβολή':
                return HttpResponseRedirect(reverse('employee_list'))
            #if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                #form = EmployeeFormCore(error_class=DivErrorList)            
    else:
        form = EmployeeFormCore(error_class=DivErrorList)            
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.change_employee')
def employee_form_update_core(request, employee_id, template_name="hr/employee_form_core.html"):
    title='Update Employee Core'
    saved=False
    if request.method == 'POST':
        employee = Employee.objects.get(id=employee_id)
        form = EmployeeFormCoreUpdate(request.POST, request.FILES, instance=employee, error_class=DivErrorList)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.updated_by = request.user
            employee.save()
            saved=True
            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                redirect = '%s#tab1' % (rev,)
                return HttpResponseRedirect(redirect)            
            #if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                #form = EmployeeFormCoreUpdate(error_class=DivErrorList)            
    else:
        employee = Employee.objects.get(id=employee_id)
        form = EmployeeFormCoreUpdate(instance=employee, error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.change_employee')
def employee_form_update_extra(request, employee_id, template_name="hr/employee_form_extra.html"):
    title='Update Employee Extra'
    saved=False
    if request.method == 'POST':
        employee = Employee.objects.get(id=employee_id)
        form = EmployeeFormExtra(request.POST, instance=employee, error_class=DivErrorList)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.updated_by = request.user
            employee.save()
            saved=True
            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                redirect = '%s#tab2' % (rev,)
                return HttpResponseRedirect(redirect)            
            #if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                #form = EmployeeFormExtra(error_class=DivErrorList)            
    else:
        employee = Employee.objects.get(id=employee_id)
        form = EmployeeFormExtra(instance=employee, error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def employee_detail(request, employee_slug, template_name="hr/employee_detail.html"):
    title='View Employee'
    employee= get_object_or_404(Employee, id=employee_slug)
    persons=employee.person_set.all()
    personal_phones=employee.phone_set.filter(phone_type='P')
    work_phones=employee.phone_set.filter(phone_type='W')
    emergency_phones=employee.phone_set.filter(phone_type='E')
    personal_emails=employee.email_set.filter(email_type='P')
    work_emails=employee.email_set.filter(email_type='W')
    work_histories=employee.workhistory_set.all().order_by('date_fm')
    educations=employee.education_set.all()
    foreign_languages = employee.foreignlanguage_set.all()
    try:
        latest_work_history = work_histories.order_by('-date_fm')[0]
        current_work_history = latest_work_history
        if current_work_history.org_workplace:
            ancestors = current_work_history.org_workplace.get_ancestors()[1:]
    except IndexError:
        pass
    """
    try:
        latest_work_history = work_histories.get(date_to=None)
        current_work_history = latest_work_history
        if current_work_history.org_workplace:
            ancestors = current_work_history.org_workplace.get_ancestors()[1:]
    except ObjectDoesNotExist:
        pass
    """
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def employee_list(request, template_name="hr/employee_list.html"):
    title='List Employee'
    sort = Employee._meta.ordering[0] #@UndefinedVariable
    #sort = 'name'  #default sort
    if 'sort' in request.GET:
        sort = request.GET['sort']
        
    pref = request.user.get_profile().employee_filter_preference
    employee_filter = None
    if pref == 'ACTIVE':
        employee_filter = True
        employees = Employee.objects.filter(is_active=employee_filter).order_by(sort)
    if pref == 'INACTIVE':
        employee_filter = False
        employees = Employee.objects.filter(is_active=employee_filter).order_by(sort)
    if pref == 'ALL':
        employees = Employee.objects.order_by(sort)    
    
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.delete_employee')
def employee_delete(request, employee_id):
    #deleted=False
    employee= get_object_or_404(Employee, id=employee_id)
    employee.delete()
    #deleted=True
    return HttpResponseRedirect(reverse('employee_list'))            

@login_required
@permission_required('hr.change_employee')
def person_formset_update(request, employee_id, template_name="hr/person_formset.html"):
    title='Ενημέρωση Προστατευόμενου Μέλους'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    PersonFormSet = modelformset_factory(Person, PersonForm, extra=0)
    if request.method == 'POST':
        """
        post = request.POST.copy()
        formset = PersonFormSet(post, error_class=DivErrorList)
        i=0
        while (i<formset.initial_form_count()):
            key ='form-%s-employee' % i
            post[key] = employee_id
            i=i+1
        """
        formset = PersonFormSet(request.POST, error_class=DivErrorList)
        if formset.is_valid():
            person_instances = formset.save(commit=False)
            for person in person_instances:
                person.updated_by = request.user
                person.employee = Employee.objects.get(id=employee_id)
                person.save()
                saved=True            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                redirect = '%s#tab6' % (rev,)
                return HttpResponseRedirect(redirect)            
    else:
        formset = PersonFormSet(error_class=DivErrorList, queryset=Person.objects.filter(employee__id=employee_id))
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.add_person')
def person_form_add(request, employee_id, template_name="hr/person_form.html"):
    title='Προσθήκη Προστατευόμενου Μέλους'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        """
        post = request.POST.copy()
        post['employee'] = employee_id
        """
        form = PersonForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            person = form.save(commit=False)
            person.created_by = request.user
            person.employee = Employee.objects.get(id=employee_id)
            person.save()
            saved=True
            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                redirect = '%s#tab6' % (rev,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                form = PersonForm(error_class=DivErrorList)            
    else:
        form = PersonForm(error_class=DivErrorList)            
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.change_person')
def person_form_update(request, employee_id, person_id, template_name="hr/person_form.html"):
    title='Ενημέρωση Προστατευόμενου Μέλους'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        person = Person.objects.get(id=person_id)
        form = PersonForm(request.POST, instance=person, error_class=DivErrorList)
        if form.is_valid():
            person = form.save(commit=False)
            person.updated_by = request.user
            person.employee = Employee.objects.get(id=employee_id)
            person.save()
            saved=True
            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                redirect = '%s#tab6' % (rev,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                return HttpResponseRedirect(reverse('person_form_add', kwargs={'employee_id': employee_id}))            
    else:
        person = Person.objects.get(id=person_id)
        form = PersonForm(instance=person, error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.delete_person')
def person_delete(request, employee_id, person_id):
    #deleted=False
    person= get_object_or_404(Person, id=person_id)
    person.delete()
    #deleted=True
    rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
    redirect = '%s#tab6' % (rev,)
    return HttpResponseRedirect(redirect)            

@login_required
@permission_required('hr.change_phone')
def phone_formset_update(request, employee_id, phone_type, template_name="hr/phone_formset.html"):
    title='Ενημέρωση Τηλεφώνου'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    tab='tab3'
    PhoneFormSet = modelformset_factory(Phone, PhoneForm, extra=0)
    if request.method == 'POST':
        formset = PhoneFormSet(request.POST, error_class=DivErrorList)
        if formset.is_valid():
            phone_instances = formset.save(commit=False)
            for phone in phone_instances:
                phone.updated_by = request.user
                phone.employee = Employee.objects.get(id=employee_id)
                phone.save()
                saved=True            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                if phone_type=='W':
                    tab='tab3'
                if phone_type=='P':
                    tab='tab4'
                if phone_type=='E':
                    tab='tab5'
                redirect = '%s#%s' % (rev,tab,)
                return HttpResponseRedirect(redirect)            
    else:
        formset = PhoneFormSet(error_class=DivErrorList, queryset=Phone.objects.filter(employee__id=employee_id, phone_type=phone_type))
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.add_phone')
def phone_form_add(request, employee_id, phone_type, template_name="hr/phone_form.html"):
    title='Προσθήκη Τηλεφώνου'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    tab='tab3'
    if request.method == 'POST':
        if phone_type=='E':
            form = PhoneFormEmergency(request.POST, error_class=DivErrorList)
        else:         
            form = PhoneForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            phone = form.save(commit=False)
            phone.created_by = request.user
            phone.employee = Employee.objects.get(id=employee_id)
            phone.phone_type=phone_type
            phone.save()
            saved=True            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                if phone_type=='W':
                    tab='tab3'
                if phone_type=='P':
                    tab='tab4'
                if phone_type=='E':
                    tab='tab5'
                redirect = '%s#%s' % (rev,tab,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                if phone_type=='E':
                    form = PhoneFormEmergency(error_class=DivErrorList)            
                else:
                    form = PhoneForm(error_class=DivErrorList)            
    else:
        if phone_type=='E':
            form = PhoneFormEmergency(error_class=DivErrorList)            
        else:
            form = PhoneForm(error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.change_phone')
def phone_form_update(request, employee_id, phone_id, template_name="hr/phone_form.html"):
    title='Ενημέρωση Τηλεφώνου'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    tab='tab3'
    if request.method == 'POST':
        phone = Phone.objects.get(id=phone_id)
        form = PhoneForm(request.POST, instance=phone, error_class=DivErrorList)
        if form.is_valid():
            phone = form.save(commit=False)
            phone.updated_by = request.user
            phone.employee = Employee.objects.get(id=employee_id)
            phone.save()
            saved=True
            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                if phone.phone_type=='W':
                    tab='tab3'
                if phone.phone_type=='P':
                    tab='tab4'
                if phone.phone_type=='E':
                    tab='tab5'
                redirect = '%s#%s' % (rev,tab,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                return HttpResponseRedirect(reverse('phone_form_add', kwargs={'employee_id': employee_id, 'phone_type': phone.phone_type}))            
    else:
        phone = Phone.objects.get(id=phone_id)
        form = PhoneForm(instance=phone, error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.delete_phone')
def phone_delete(request, employee_id, phone_id):
    #deleted=False
    phone= get_object_or_404(Phone, id=phone_id)
    rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
    if phone.phone_type=='W':
        tab='tab3'
    if phone.phone_type=='P':
        tab='tab4'
    if phone.phone_type=='E':
        tab='tab5'
    redirect = '%s#%s' % (rev,tab,)
    phone.delete()
    #deleted=True
    return HttpResponseRedirect(redirect)            

@login_required
@permission_required('hr.change_email')
def email_formset_update(request, employee_id, email_type, template_name="hr/email_formset.html"):
    title='Ενημέρωση Email'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    tab='tab3'
    EmailFormSet = modelformset_factory(Email, EmailForm, extra=0)
    if request.method == 'POST':
        formset = EmailFormSet(request.POST, error_class=DivErrorList)
        if formset.is_valid():
            email_instances = formset.save(commit=False)
            for email in email_instances:
                email.updated_by = request.user
                email.employee = Employee.objects.get(id=employee_id)
                email.save()
                saved=True            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                if email_type=='W':
                    tab='tab3'
                if email_type=='P':
                    tab='tab4'
                redirect = '%s#%s' % (rev,tab,)
                return HttpResponseRedirect(redirect)            
    else:
        formset = EmailFormSet(error_class=DivErrorList, queryset=Email.objects.filter(employee__id=employee_id, email_type=email_type))
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.add_email')
def email_form_add(request, employee_id, email_type, template_name="hr/email_form.html"):
    title='Προσθήκη Email'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    tab='tab3'
    if request.method == 'POST':
        form = EmailForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            email = form.save(commit=False)
            email.created_by = request.user
            email.employee = Employee.objects.get(id=employee_id)
            email.email_type=email_type
            email.save()
            saved=True            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                if email_type=='W':
                    tab='tab3'
                if email_type=='P':
                    tab='tab4'
                redirect = '%s#%s' % (rev,tab,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                form = EmailForm(error_class=DivErrorList)            
    else:
        form = EmailForm(error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.change_email')
def email_form_update(request, employee_id, email_id, template_name="hr/email_form.html"):
    title='Ενημέρωση Email'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    tab='tab3'
    if request.method == 'POST':
        email = Email.objects.get(id=email_id)
        form = EmailForm(request.POST, instance=email, error_class=DivErrorList)
        if form.is_valid():
            email = form.save(commit=False)
            email.updated_by = request.user
            email.employee = Employee.objects.get(id=employee_id)
            email.save()
            saved=True
            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                if email.email_type=='W':
                    tab='tab3'
                if email.email_type=='P':
                    tab='tab4'
                redirect = '%s#%s' % (rev,tab,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                return HttpResponseRedirect(reverse('email_form_add', kwargs={'employee_id': employee_id, 'email_type': email.email_type}))            
    else:
        email = Email.objects.get(id=email_id)
        form = EmailForm(instance=email, error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.delete_email')
def email_delete(request, employee_id, email_id):
    #deleted=False
    email= get_object_or_404(Email, id=email_id)
    rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
    if email.email_type=='W':
        tab='tab3'
    if email.email_type=='P':
        tab='tab4'
    redirect = '%s#%s' % (rev,tab,)
    email.delete()
    #deleted=True
    return HttpResponseRedirect(redirect)            

@login_required
def employee_chart_list(request, template_name="hr/employee_chart_list.html", employee_code=None):
    title='List Employee Chart'
    sort = 'employee__id'
    if 'sort' in request.GET:
        sort = request.GET['sort']
        sort = u'employee__%s' % (sort,)
        
    pref = request.user.get_profile().employee_filter_preference
    employee_filter = None
    node_list = Chart.objects.get(code = employee_code).get_code_list()
    if pref == 'ACTIVE':
        employee_filter = True
        work_histories = WorkHistory.objects.filter(Q(employee__is_active=employee_filter), Q(org_workplace__code__in = node_list), Q(date_fm__lte=settings.QUERY_DATE) , Q(date_to__gte=settings.QUERY_DATE) | Q(date_to=None)).order_by(sort)
    if pref == 'INACTIVE':
        employee_filter = False
        work_histories = WorkHistory.objects.filter(Q(employee__is_active=employee_filter), Q(org_workplace__code__in = node_list), Q(date_fm__lte=settings.QUERY_DATE) , Q(date_to__gte=settings.QUERY_DATE) | Q(date_to=None)).order_by(sort)
    if pref == 'ALL':
        work_histories = WorkHistory.objects.filter(Q(org_workplace__code__in = node_list), Q(date_fm__lte=settings.QUERY_DATE) , Q(date_to__gte=settings.QUERY_DATE) | Q(date_to=None)).order_by(sort)
    
    #work_histories = WorkHistory.objects.filter(org_workplace__code=employee_code, date_to=None).order_by(sort)
    
    #work_histories = WorkHistory.objects.filter(org_workplace__code=employee_code).values('employee').annotate(latest = Max('date_fm')).order_by()

    """
    employees = Employee.objects.all()
    # create empty queryset hack
    #latest_work_histories = WorkHistory.objects.extra(where=['1=0'])
    latest_work_histories = WorkHistory.objects.filter(date_fm__year='1000')
    for employee in employees:
        work_histories=employee.workhistory_set.filter(org_workplace__code=employee_code)
        date = None
        for work_history in work_histories:
            if date is None:
                date = work_history.date_fm
            else:
                if date < work_history.date_fm:
                    date = work_history.date_fm
        work_histories = work_histories.filter(date_fm=date)          
        if work_histories:
            latest_work_histories = latest_work_histories | work_histories
    work_histories = latest_work_histories.order_by(sort)
    """
    code = employee_code
    nodes = Chart.objects.all()      
    node_title = get_object_or_404(Chart, code=employee_code).title
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.add_workhistory')
def workhistory_form_add(request, employee_id, template_name="hr/workhistory_form.html"):
    title='Προσθήκη Ιστορικού Εργασίας'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        post = request.POST.copy()
        post['employee'] = employee_id
        form = WorkHistoryForm(post, error_class=DivErrorList)
        if form.is_valid():
            work_history = form.save(commit=False)
            work_history.created_by = request.user
            work_history.employee = Employee.objects.get(id=employee_id)
            work_history.save()
            saved=True            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                redirect = '%s#tab7' % (rev,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                form = WorkHistoryForm(error_class=DivErrorList)            
    else:
        form = WorkHistoryForm(error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.change_workhistory')
def workhistory_form_update(request, employee_id, work_history_id, template_name="hr/workhistory_form.html"):
    title='Ενημέρωση Ιστορικού Εργασίας'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        work_history = WorkHistory.objects.get(id=work_history_id)
        form = WorkHistoryFormUpdate(request.POST, instance=work_history, error_class=DivErrorList)
        if form.is_valid():
            work_history = form.save(commit=False)
            work_history.updated_by = request.user
            work_history.employee = Employee.objects.get(id=employee_id)
            work_history.save()
            saved=True
            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                redirect = '%s#tab7' % (rev,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                return HttpResponseRedirect(reverse('workhistory_form_add', kwargs={'employee_id': employee_id}))            
    else:
        work_history = WorkHistory.objects.get(id=work_history_id)
        form = WorkHistoryFormUpdate(instance=work_history, error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.delete_workhistory')
def workhistory_delete(request, employee_id, work_history_id):
    #deleted=False
    workhistory= get_object_or_404(WorkHistory, id=work_history_id)
    workhistory.delete()
    #deleted=True
    rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
    redirect = '%s#tab7' % (rev,)
    return HttpResponseRedirect(redirect)

@login_required
@permission_required('hr.add_education')
def education_form_add(request, employee_id, template_name="hr/education_form.html"):
    title='Προσθήκη Τίτλου Σπουδών'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EducationForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            education = form.save(commit=False)
            education.created_by = request.user
            education.employee = Employee.objects.get(id=employee_id)
            education.save()
            saved=True            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                redirect = '%s#tab8' % (rev,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                form = EducationForm(error_class=DivErrorList)            
    else:
        form = EducationForm(error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.change_education')
def education_form_update(request, employee_id, education_id, template_name="hr/education_form.html"):
    title='Ενημέρωση Τίτλου Σπουδών'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        education = Education.objects.get(id=education_id)
        form = EducationForm(request.POST, instance=education, error_class=DivErrorList)
        if form.is_valid():
            education = form.save(commit=False)
            education.updated_by = request.user
            education.employee = Employee.objects.get(id=employee_id)
            education.save()
            saved=True
            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                redirect = '%s#tab8' % (rev,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                return HttpResponseRedirect(reverse('education_form_add', kwargs={'employee_id': employee_id}))            
    else:
        education = Education.objects.get(id=education_id)
        form = EducationForm(instance=education, error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.delete_education')
def education_delete(request, employee_id, education_id):
    #deleted=False
    education= get_object_or_404(Education, id=education_id)
    education.delete()
    #deleted=True
    rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
    redirect = '%s#tab8' % (rev,)
    return HttpResponseRedirect(redirect)

@login_required
@permission_required('hr.add_foreignlanguage')
def foreign_language_form_add(request, employee_id, template_name="hr/foreign_language_form.html"):
    title='Προσθήκη Ξένης Γλώσσας'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = ForeignLanguageForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            foreign_language = form.save(commit=False)
            foreign_language.created_by = request.user
            foreign_language.employee = Employee.objects.get(id=employee_id)
            foreign_language.save()
            saved=True            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                redirect = '%s#tab8' % (rev,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                form = ForeignLanguageForm(error_class=DivErrorList)            
    else:
        form = ForeignLanguageForm(error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.change_foreignlanguage')
def foreign_language_form_update(request, employee_id, foreign_language_id, template_name="hr/foreign_language_form.html"):
    title='Ενημέρωση Ξένης Γλώσσας'
    saved=False
    employee= get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        foreign_language = ForeignLanguage.objects.get(id=foreign_language_id)
        form = ForeignLanguageForm(request.POST, instance=foreign_language, error_class=DivErrorList)
        if form.is_valid():
            foreign_language = form.save(commit=False)
            foreign_language.updated_by = request.user
            foreign_language.employee = Employee.objects.get(id=employee_id)
            foreign_language.save()
            saved=True
            
            if request.POST['submit']=='Υποβολή':
                rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
                redirect = '%s#tab8' % (rev,)
                return HttpResponseRedirect(redirect)            
            if request.POST['submit']=='Υποβολή και Προσθήκη Νέου':
                return HttpResponseRedirect(reverse('foreign_language_form_add', kwargs={'employee_id': employee_id}))            
    else:
        foreign_language = ForeignLanguage.objects.get(id=foreign_language_id)
        form = ForeignLanguageForm(instance=foreign_language, error_class=DivErrorList)
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@permission_required('hr.delete_foreignlanguage')
def foreign_language_delete(request, employee_id, foreign_language_id):
    #deleted=False
    foreign_language= get_object_or_404(ForeignLanguage, id=foreign_language_id)
    foreign_language.delete()
    #deleted=True
    rev = reverse('employee_detail', kwargs={'employee_slug': employee_id})
    redirect = '%s#tab8' % (rev,)
    return HttpResponseRedirect(redirect)

        

          
