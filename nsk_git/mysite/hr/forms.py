# -*- coding: utf-8 -*-
import re
from django.forms import ModelForm, TextInput, Textarea, DateInput, Select, CheckboxInput, FileInput, ValidationError
from django.forms.util import ErrorList
from mysite.hr.models import Employee, Person, Phone, Email, WorkHistory, Education, ForeignLanguage
from mysite.mgmt.models import Country, Language
from mysite.organization_chart.models import Chart
from django.db.models import F

class EmployeeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
                        
    class Meta:
        model = Employee
        
class EmployeeFormCore(EmployeeForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeFormCore, self).__init__(*args, **kwargs)
        self.fields['birthdate'].widget.format = '%d/%m/%Y'
        self.fields['birthdate'].input_formats = ['%d/%m/%Y']
        self.fields['birth_country'].queryset = Country.objects.filter(is_active=True)        
        self.fields['city'].queryset = Country.objects.filter(is_active=True)        
        self.fields['addr_country'].queryset = Country.objects.filter(is_active=True)
        #self.fields['gender'].empty_label = ''
        self.fields['birth_country'].empty_label = ''
        #self.fields['marital_status'].empty_label = ''
        self.fields['addr_country'].empty_label = ''
    class Meta(EmployeeForm.Meta):
        widgets = {
            'employee_id': TextInput(attrs={'required': 'required', 'tabindex': '1'}),
            'name': TextInput(attrs={'required': 'required', 'tabindex': '2'}),
            'surname': TextInput(attrs={'required': 'required', 'tabindex': '3'}),
            'father_name': TextInput(attrs={'tabindex': '4'}),
            'mother_name': TextInput(attrs={'tabindex': '5'}),
            'mother_surname': TextInput(attrs={'tabindex': '6'}),
            'gender': Select(attrs={'tabindex': '7'}),
            'birthdate': DateInput(attrs={'tabindex': '8'}),
            'birth_country': Select(attrs={'tabindex': '9'}),
            'marital_status': Select(attrs={'tabindex': '10'}),
            'husband_name': TextInput(attrs={'tabindex': '11'}),
            'husband_surname': TextInput(attrs={'tabindex': '12'}),
            'address': TextInput(attrs={'tabindex': '13'}),
            'address_opt': TextInput(attrs={'tabindex': '14'}),
            'zipcode': TextInput(attrs={'tabindex': '15'}),
            'city': TextInput(attrs={'tabindex': '16'}),
            'addr_country': Select(attrs={'tabindex': '17'}),
            'militarySvc_liableTo': CheckboxInput(attrs={'tabindex': '18'}),
            'disability': CheckboxInput(attrs={'tabindex': '19'}),
            'photo': FileInput(attrs={'tabindex': '20'}),
        }
        fields={'employee_id', 'name', 'surname', 'father_name', 'mother_name', 'mother_surname', 'marital_status',
                  'husband_name', 'husband_surname', 'gender', 'birthdate', 'birth_country', 'address',
                   'address_opt', 'zipcode', 'city', 'addr_country', 'militarySvc_liableTo', 'disability', 'photo'}

class EmployeeFormCoreUpdate(EmployeeFormCore):
    def __init__(self, *args, **kwargs):
        super(EmployeeFormCoreUpdate, self).__init__(*args, **kwargs)
        self.fields['birthdate'].widget.format = '%d/%m/%Y'
        self.fields['birthdate'].input_formats = ['%d/%m/%Y']
        self.fields['birth_country'].queryset = Country.objects.filter(is_active=True)        
        self.fields['city'].queryset = Country.objects.filter(is_active=True)        
        self.fields['addr_country'].queryset = Country.objects.filter(is_active=True)        
        self.fields['employee_id'].widget.attrs['readonly'] = 'readonly'

class EmployeeFormExtra(EmployeeForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeFormExtra, self).__init__(*args, **kwargs)
        self.fields['idc_issue_date'].widget.format = '%d/%m/%Y'
        self.fields['idc_issue_date'].input_formats = ['%d/%m/%Y']
        self.fields['idc_exp_date'].widget.format = '%d/%m/%Y'
        self.fields['idc_exp_date'].input_formats = ['%d/%m/%Y']
        self.fields['dLic_issue_date'].widget.format = '%d/%m/%Y'
        self.fields['dLic_issue_date'].input_formats = ['%d/%m/%Y']
        self.fields['dLic_exp_date'].widget.format = '%d/%m/%Y'
        self.fields['dLic_exp_date'].input_formats = ['%d/%m/%Y']
        self.fields['idc_country'].queryset = Country.objects.filter(is_active=True)        
        self.fields['dLic_country'].queryset = Country.objects.filter(is_active=True)        
        self.fields['idc_type'].empty_label = ''
        self.fields['idc_country'].empty_label = ''
        self.fields['dLic_type'].empty_label = ''
        self.fields['dLic_country'].empty_label = ''
    class Meta(EmployeeForm.Meta):
        fields={'idc_number', 'idc_type', 'idc_country', 'idc_issue_date', 'idc_exp_date', 'idc_comment',
                  'taxID_number', 'taxOffice_number', 'taxOffice_desc', 'SSN', 'idc_IKA', 'dLic_number', 'dLic_type',
                   'dLic_country', 'dLic_issue_date', 'dLic_exp_date', 'dLic_comment'}

    def clean_taxID_number(self):
        data = self.cleaned_data['taxID_number']
        match = re.search(r'^\d{9}$|^$',data)
        if not match:
            raise ValidationError("Μή έγκυρος Α.Φ.Μ.")
        # Always return the cleaned data, whether you have changed it or not.
        return data

    def clean_SSN(self):
        data = self.cleaned_data['SSN']
        match = re.search(r'^\d{11}$|^$',data)
        if not match:
            raise ValidationError("Μή έγκυρος Α.Μ.Κ.Α.")
        return data

    def clean_idc_IKA(self):
        data = self.cleaned_data['idc_IKA']
        match = re.search(r'^\d{8}$|^$',data)
        if not match:
            raise ValidationError("Μή έγκυρος αριθμός μητρώου Ι.Κ.Α.")
        return data

class PersonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['birthdate'].widget.format = '%d/%m/%Y'
        self.fields['birthdate'].input_formats = ['%d/%m/%Y']
        self.fields['date_fm'].widget.format = '%d/%m/%Y'
        self.fields['date_fm'].input_formats = ['%d/%m/%Y']
        self.fields['date_to'].widget.format = '%d/%m/%Y'
        self.fields['date_to'].input_formats = ['%d/%m/%Y']
        self.fields['relation'].empty_label = ''
        self.fields['working_status'].empty_label = ''
        #self.fields['employee'].widget.attrs['disabled'] = 'disabled'
    class Meta:
        model = Person
        widgets = {
            'name': TextInput(attrs={'required': 'required'}),
            'surname': TextInput(attrs={'required': 'required'}),
        }        
        fields={'name', 'surname', 'birthdate', 'relation', 'disability', 'disability_rate', 'working_status',
                  'comment', 'date_fm', 'date_to'}

class PhoneForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhoneForm, self).__init__(*args, **kwargs)
        self.fields['phone_kind'].empty_label = ''
    class Meta:
        model = Phone
        widgets = {
            'phone_number': TextInput(attrs={'required': 'required'}),
            'comment': Textarea(attrs={'rows':4, 'cols':60}),
        }
        fields={'phone_number', 'phone_kind', 'comment'}

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        match = re.search(r'^[+]?[\d]+[\d\s]*$',data)
        if not match:
            raise ValidationError("Μή έγκυρος αριθμός τηλεφώνου.")
        return data
        
class PhoneFormEmergency(PhoneForm):
    def __init__(self, *args, **kwargs):
        super(PhoneFormEmergency, self).__init__(*args, **kwargs)
        self.fields['person'].empty_label = ''
    class Meta(PhoneForm.Meta):
        fields={'phone_number', 'phone_kind', 'comment', 'person'}
             
class EmailForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Email
        widgets = {
            'email': TextInput(attrs={'required': 'required'}),
            'comment': Textarea(attrs={'rows':4, 'cols':60}),
        }
        fields={'email', 'comment'}
        
class WorkHistoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkHistoryForm, self).__init__(*args, **kwargs)
        self.fields['date_fm'].widget.format = '%d/%m/%Y'
        self.fields['date_fm'].input_formats = ['%d/%m/%Y']
        self.fields['date_to'].widget.format = '%d/%m/%Y'
        self.fields['date_to'].input_formats = ['%d/%m/%Y']
        self.fields['org_workplace'].queryset = Chart.objects.filter(lft=F('rght')-1)        
        self.fields['speciality'].empty_label = ''
        self.fields['org_position'].empty_label = ''
        self.fields['org_workplace'].empty_label = ''
    class Meta:
        model = WorkHistory
        widgets = {
            'date_fm': DateInput(attrs={'required': 'required', 'id': 'datepicker'}),
        }        
        fields={'employee', 'speciality', 'org_position', 'org_workplace', 'date_fm', 'date_to'}

    def clean(self):
        cleaned_data = super(WorkHistoryForm, self).clean()
        date_fm = cleaned_data.get("date_fm")
        date_to = cleaned_data.get("date_to")
        employee = cleaned_data.get("employee")
        #employee = self.instance.employee

        if date_fm is None:
            return cleaned_data            

        work_histories=employee.workhistory_set.all().order_by('date_fm')        
        validate_work_history(cleaned_data, date_fm, date_to, employee, work_histories)
        return cleaned_data                                                              

class WorkHistoryFormUpdate(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkHistoryFormUpdate, self).__init__(*args, **kwargs)
        self.fields['date_fm'].widget.format = '%d/%m/%Y'
        self.fields['date_fm'].input_formats = ['%d/%m/%Y']
        self.fields['date_to'].widget.format = '%d/%m/%Y'
        self.fields['date_to'].input_formats = ['%d/%m/%Y']
        self.fields['org_workplace'].queryset = Chart.objects.filter(lft=F('rght')-1)        
        self.fields['speciality'].empty_label = ''
        self.fields['org_position'].empty_label = ''
        self.fields['org_workplace'].empty_label = ''
    class Meta:
        model = WorkHistory
        widgets = {
            'date_fm': DateInput(attrs={'required': 'required'}),
        }        
        fields={'employee', 'speciality', 'org_position', 'org_workplace', 'date_fm', 'date_to'}

    def clean(self):
        cleaned_data = super(WorkHistoryFormUpdate, self).clean()
        date_fm = cleaned_data.get("date_fm")
        date_to = cleaned_data.get("date_to")
        #employee = cleaned_data.get("employee")
        employee = self.instance.employee
        
        if date_fm is None:
            return cleaned_data            

        work_histories=employee.workhistory_set.exclude(id=self.instance.pk).order_by('date_fm')
        if not work_histories:
            return cleaned_data                                                              
        validate_work_history(cleaned_data, date_fm, date_to, employee, work_histories)
        return cleaned_data
    
class EducationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        self.fields['swearing_in_date'].widget.format = '%d/%m/%Y'
        self.fields['swearing_in_date'].input_formats = ['%d/%m/%Y']
        self.fields['edu_country'].queryset = Country.objects.filter(is_active=True)        
        self.fields['edu_country'].empty_label = ''
        #self.fields['degree_type'].empty_label = ''
    class Meta:
        model = Education
        widgets = {
            'diploma': TextInput(attrs={'required': 'required'}),
        }        
        fields={'diploma', 'degree_type', 'faculty',  'semesters', 'swearing_in_date', 'edu_country'}                                                          

class ForeignLanguageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ForeignLanguageForm, self).__init__(*args, **kwargs)
        self.fields['acquirement_date'].widget.format = '%d/%m/%Y'
        self.fields['acquirement_date'].input_formats = ['%d/%m/%Y']
        self.fields['language'].empty_label = ''
        self.fields['language'].queryset = Language.objects.filter(is_active=True)        
    class Meta:
        model = ForeignLanguage
        widgets = {
            'language': Select(attrs={'required': 'required'}),
        }        
        fields={'language', 'diploma', 'acquirement_date'}                                                          

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        #return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])
        return ''.join([u'<div class="ym-message">%s</div>' % e for e in self])

def validate_work_history(cleaned_data, date_fm, date_to, employee, work_histories):
    if employee and date_fm:           
        if date_to is None:
            #work_histories=employee.workhistory_set.all()
            for work_history in work_histories:
                if work_history.date_to is None:
                    raise ValidationError("date_to=None already exists")
                if work_history.date_fm > date_fm:
                    raise ValidationError("date_fm invalid")
            return cleaned_data                                                              
        else:
            if date_fm >= date_to:
                raise ValidationError("date_to must be greater than date_fm")
     
    if employee and date_fm:
        #work_histories=employee.workhistory_set.all().order_by('date_fm')                                                                     
        id_list = list(work_histories.values_list('id', flat=True))
        if not id_list:
            return cleaned_data                                                              
        else:
            first_work_history = work_histories.get(id=id_list[0])
            if date_to < first_work_history.date_fm:
                return cleaned_data                                              
        for work_history in work_histories:
            try:
                next_id = id_list[id_list.index(work_history.id) + 1]
                next_work_history = work_histories.get(id=next_id)
                if date_fm > work_history.date_to and date_to < next_work_history.date_fm:
                    return cleaned_data
            except IndexError:
                if work_history.date_to is None:
                    raise ValidationError("Field overlap")
                if date_fm > work_history.date_to:
                    return cleaned_data                          
        raise ValidationError("Field overlap")
    # Always return the full collection of cleaned data.      
    return cleaned_data
