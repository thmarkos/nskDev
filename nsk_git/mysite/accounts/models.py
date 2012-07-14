# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    EMPLOYEE_FILTER_CHOICES = (
        (u'ACTIVE', u'Ενεργοί'),
        (u'INACTIVE', u'Μη Ενεργοί'),
        (u'ALL', u'Όλοι'),
    )
    employee_filter_preference = models.CharField("Προτιμήσεις Προβολής Εργαζομένων", max_length=10, choices=EMPLOYEE_FILTER_CHOICES, default='ACTIVE')
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)