# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from mysite.mgmt.models import Country, IDC, DLic, Relation, WorkingStatus, Kind, Speciality, OrgPosition, Language
from mysite.organization_chart.models import Chart

class Employee(models.Model):
    """ Basic Data"""
    employee_id = models.IntegerField("Αριθμός Μητρώου")
    name = models.CharField("Όνομα", max_length=20)
    surname = models.CharField("Επώνυμο", max_length=20)
    photo = models.ImageField("Φωτογραφία", upload_to='photo/employee', default='photo/employee/bird.jpg')
    father_name = models.CharField("Όνομα Πατέρα", max_length=20, blank=True)
    mother_name = models.CharField("Όνομα Μητέρας", max_length=20, blank=True)
    mother_surname = models.CharField("Γένος Μητέρας", max_length=20, blank=True)
    husband_name = models.CharField("Όνομα Συζύγου", max_length=20, blank=True)
    husband_surname = models.CharField("Επώνυμο Συζύγου", max_length=20, blank=True)
    MARITAL_CHOICES = (
        (u'S', u'Άγαμ(ος)η'),
        (u'M', u'Έγγαμ(ος)η'),
        (u'D', u'Διαζευγμέν(ος)η'),
        (u'W', u'Χήρ(ος)α'),
    )
    marital_status = models.CharField("Οικογ. Κατάσταση", max_length=2, choices=MARITAL_CHOICES, blank=True)
    """ Basic Data 2 """
    birthdate = models.DateField("Ημερομηνία Γέννησης", blank=True, null=True)
    birth_country = models.ForeignKey(Country, blank=True, null=True, verbose_name="Χώρα Γέννησης", related_name='employee_birth_country')
    GENDER_CHOICES = (
        (u'M', u'Αρσενικό'),
        (u'F', u'Θηλυκό'),
    )
    gender = models.CharField("Φύλο", max_length=1, choices=GENDER_CHOICES, blank=True)
    """ Address Data """
    address = models.CharField("Οδός - Αριθμός", max_length = 30, blank=True)
    address_opt = models.CharField("Περιοχή", max_length = 30, blank=True)
    zipcode = models.CharField("Τ.Κ.", max_length = 10, blank=True)
    city = models.CharField("Πόλη", max_length = 20, blank=True)
    addr_country = models.ForeignKey(Country, blank=True, null=True, verbose_name="Χώρα", related_name='employee_addr_country')
    """ ID Data """
    idc_country = models.ForeignKey(Country, blank=True, null=True, verbose_name="Χώρα Έκδοσης", related_name='employee_idc_country')
    idc_type = models.ForeignKey(IDC, blank=True, null=True, verbose_name="Τύπος")
    idc_number = models.CharField("Αριθμός Ταυτότητας", max_length = 15, blank=True, null=True)
    idc_issue_date = models.DateField("Ημερομηνία Έκδοσης", blank=True, null=True)
    idc_exp_date = models.DateField("Ημερομηνία Λήξης", blank=True, null=True)
    idc_comment = models.CharField("Παρατηρήσεις", max_length = 20, blank=True)
    """ Tax Data"""
    taxID_number = models.CharField("Α.Φ.Μ", max_length = 15, blank=True, null=True)
    taxOffice_number = models.CharField("Κωδικός Εφορίας", max_length = 10, blank=True, null=True)
    taxOffice_desc = models.CharField("Περιγραφή Εφορίας", max_length = 20, blank=True)
    """ SS Data"""    
    SSN = models.CharField("Α.Μ.Κ.Α", max_length = 15, blank=True, null=True)
    idc_IKA = models.CharField("Αριθμός Μητρώου Ι.Κ.Α.", max_length = 20, blank=True)
    """ Other Pesonal Data"""
    disability = models.BooleanField("Α.Μ.Ε.Α", default=False)
    militarySvc_liableTo = models.BooleanField("Υπόχρεος Στράτευσης", default=False)
    """ Driver's lincence Data"""
    dLic_country = models.ForeignKey(Country, blank=True, null=True, verbose_name="Χώρα Έκδοσης", related_name='employee_dLic_country')
    dLic_type = models.ForeignKey(DLic, blank=True, null=True, verbose_name="Τύπος")
    dLic_number = models.CharField("Αριθμός Άδειας Οδήγησης", max_length = 15, blank=True, null=True)
    dLic_issue_date = models.DateField("Ημερομηνία Έκδοσης", blank=True, null=True)
    dLic_exp_date = models.DateField("Ημερομηνία Λήξης", blank=True, null=True)
    dLic_comment = models.CharField("Παρατηρήσεις", max_length = 20, blank=True)
    """ Extra """
    #hire_date = models.DateField()
    #fire_date = models.DateField()
    #max_efhmeries = models.IntegerField(verbose_name= "orio efhmeriwn ana mhna", max_length = 2)
    
    """ Metadata """
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='employee_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='employee_updated_by')
    is_active = models.BooleanField(default=True)
    #slug = models.SlugField(max_length=20, unique=True, editable=False, help_text='Unique value for employee page URL, created from name.')
       
    class Meta:
        verbose_name = "Εργαζόμενος"
        verbose_name_plural = "Εργαζόμενοι"
        ordering = ['surname']
        permissions = (
            ("can_view_private_data", "Can view private data"),
        )

    def save(self, *args, **kwargs):
        """overriding save method so that we can save Null to database, instead of empty string for fields in allow_null tuple (project requirement)"""
        # get a list of all model fields (i.e. self._meta.fields)...
        allow_null = ('idc_number', 'taxID_number', 'SSN', 'dLic_number',)
        emptystringfields = [ field for field in self._meta.fields \
                             # ...that are in tuple allow_null...
                             if (field.name in allow_null) \
                             # ...and that contain the empty string
                             and (getattr(self, field.name) == "") ]
        # set each of these fields to None (which tells Django to save Null)
        for field in emptystringfields:
            setattr(self, field.name, None)
        # call the super.save() method           
        super(Employee, self).save(*args, **kwargs)
        #self.slug = slugify(self.id)#error don't have access to self.id before it gets saved to db
                        
    def __unicode__(self):
        return u'%s %s' % (self.name, self.surname)
                
    def get_verbose_name(self, field):
        return self._meta.get_field(field).verbose_name

    @models.permalink
    def get_absolute_url(self):
        return ('employee_detail', (), { 'employee_slug': self.id })
        
class Person(models.Model):
    employee = models.ForeignKey(Employee, blank=True, null=True)
    relation = models.ForeignKey(Relation, blank=True, null=True, verbose_name="Σχέση")
    working_status = models.ForeignKey(WorkingStatus, blank=True, null=True, verbose_name="Απασχόληση")
    name = models.CharField("Όνομα", max_length=20)
    surname = models.CharField("Επώνυμο", max_length=20)
    birthdate = models.DateField("Ημερομηνία Γέννησης", blank=True, null=True)
    date_fm = models.DateField("Σε ισχύ από", blank=True, null=True)
    date_to = models.DateField("Εώς", blank=True, null=True)
    comment = models.CharField("Σχόλιο", max_length=30, blank=True)
    disability = models.BooleanField("Α.Μ.Ε.Α", default=False)
    disability_rate = models.IntegerField("Ποσοστό Αναπηρίας", max_length=3, default=0)
    """ Metadata """
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='person_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='person_updated_by')
    is_active = models.BooleanField(default=True)
    #slug = models.SlugField(max_length=20, unique=True, editable=False, help_text='Unique value for person page URL, created from name.')

    class Meta:
        verbose_name = "person"
        verbose_name_plural = "persons"
        ordering = ['surname']

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)
                        
    def __unicode__(self):
        return u'%s %s' % (self.name, self.surname)
    
    def get_verbose_name(self, field):
        return self._meta.get_field(field).verbose_name
                
    @models.permalink
    def get_absolute_url(self):
        pass#return ('person_detail', (), { 'person_slug': self.id })

class Phone(models.Model):
    person = models.ForeignKey(Person, blank = True, null = True, verbose_name="Πρόσωπο Επικοινωνίας")
    employee = models.ForeignKey(Employee, blank = True, null = True, verbose_name="Υπάλληλος")
    
    phone_number = models.CharField("Τηλεφωνικός Αριθμός", max_length=20)
    comment = models.CharField("Σχόλιο", max_length=40, blank=True)
    
    PHONE_USE_CHOICES = (
        (u'W', u'Υπηρεσιακό'),
        (u'P', u'Προσωπικό'),
        (u'E', u'Ανάγκης'),
    )
    phone_type = models.CharField("Χρήση Τηλεφώνου", max_length=1, choices=PHONE_USE_CHOICES, default='P')
    phone_kind = models.ForeignKey(Kind, blank=True, null=True, related_name='phone_kinds', verbose_name="Είδος Τηλεφώνου")
    """ Metadata """
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='phone_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='phone_updated_by')
    is_active = models.BooleanField(default=True)
    #slug = models.SlugField(max_length=20, unique=True, editable=False, help_text='Unique value for phone page URL, created from phone_number.')

    class Meta:
        verbose_name = "Τηλέφωνο"
        verbose_name_plural = "Τηλέφωνα"
        ordering = ['phone_number']
    
    def save(self, *args, **kwargs):
        super(Phone, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.phone_number

    def get_verbose_name(self, field):
        return self._meta.get_field(field).verbose_name

    @models.permalink
    def get_absolute_url(self):
        pass#return ('show_employee', (), { 'phone_slug': self.id })
    
class Email(models.Model):
    person = models.ForeignKey(Person, blank = True, null = True, verbose_name="Πρόσωπο")
    employee = models.ForeignKey(Employee, blank = True, null = True, verbose_name="Υπάλληλος")
    
    email = models.EmailField("Διεύθυνση Email")
    comment = models.CharField("Σχόλιο", max_length=40, blank=True)
    
    EMAIL_USE_CHOICES = (
        (u'W', u'Υπηρεσιακό'),
        (u'P', u'Προσωπικό'),
    )
    email_type = models.CharField("Χρήση Email", max_length=1, choices=EMAIL_USE_CHOICES, default='P')
    """ Metadata """
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='email_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='email_updated_by')
    is_active = models.BooleanField(default=True)
    #slug = models.SlugField(max_length=20, unique=True, editable=False, help_text='Unique value for email page URL, created from email.')

    class Meta:
        verbose_name = "Διεύθυνση Email"
        verbose_name_plural = "Διευθύνσεις Email"
        ordering = ['email']
    
    def save(self, *args, **kwargs):
        super(Email, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.email

    def get_verbose_name(self, field):
        return self._meta.get_field(field).verbose_name

    @models.permalink
    def get_absolute_url(self):
        pass#return ('show_employee', (), { 'email_slug': self.id })

class WorkHistory(models.Model):
    employee = models.ForeignKey(Employee, blank = True, null = True, verbose_name="Υπάλληλος")
    speciality = models.ForeignKey(Speciality, blank = True, null = True, verbose_name="Ειδικότητα")
    org_position = models.ForeignKey(OrgPosition, blank = True, null = True, verbose_name="Θέση Ευθύνης")
    org_workplace = models.ForeignKey(Chart, blank=True, null=True, verbose_name="Χώρος Εργασίας")

    date_fm = models.DateField("Από", default=datetime.now())
    date_to = models.DateField("Εώς", blank=True, null=True)    

    """ Metadata """
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='work_history_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='work_history_updated_by')

    class Meta:
        verbose_name = "Ιστορικό Εργασίας"
        verbose_name_plural = "Ιστορικά Εργασίας"
        ordering = ['employee']

    def __unicode__(self):
        return u'%s - %s' % (self.employee, self.speciality)

    def get_verbose_name(self, field):
        return self._meta.get_field(field).verbose_name

class Education(models.Model):
    employee = models.ForeignKey(Employee, blank = True, null = True, verbose_name="Υπάλληλος")
    diploma = models.CharField("Τίτλος Σπουδών", max_length=40)
    DEGREE_TYPE_CHOICES = (
        (u'T', u'Τ.Ε.Ι.'),
        (u'A', u'Α.Ε.Ι.'),
    )
    degree_type = models.CharField("Επίπεδο Πτυχίου", max_length=1, choices=DEGREE_TYPE_CHOICES, blank=True)
    faculty = models.CharField("Σχολή", max_length=40, blank=True)
    semesters = models.IntegerField("Χρόνος Σπουδών", max_length=2, blank=True, null=True)
    swearing_in_date = models.DateField("Ημερομηνία Απόκτησης", blank=True, null=True)
    edu_country = models.ForeignKey(Country, blank=True, null=True, verbose_name="Χώρα Φοίτησης", related_name='employee_education_country')    
    
    """ Metadata """
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='education_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='education_updated_by')
    
    class Meta:
        verbose_name = "Τίτλος Σπουδών"
        verbose_name_plural = "Τίτλοι Σπουδών"
        ordering = ['employee']

    def __unicode__(self):
        return u'%s - %s' % (self.employee, self.diploma)

    def get_verbose_name(self, field):
        return self._meta.get_field(field).verbose_name
    
class ForeignLanguage(models.Model):
    employee = models.ForeignKey(Employee, blank = True, null = True, verbose_name="Υπάλληλος")
    language = models.ForeignKey(Language, verbose_name="Ξένη Γλώσσα")
    diploma = models.CharField("Τίτλος Πτυχείου", max_length=40, blank=True)
    acquirement_date = models.DateField("Ημερομηνία Απόκτησης", blank=True, null=True)
    
    """ Metadata """
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='foreign_language_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='foreign_language_updated_by')
    
    class Meta:
        verbose_name = "Ξένη Γλώσσα"
        verbose_name_plural = "Ξένες Γλώσσες"
        ordering = ['employee']

    def __unicode__(self):
        return u'%s - %s' % (self.employee, self.diploma)

    def get_verbose_name(self, field):
        return self._meta.get_field(field).verbose_name
