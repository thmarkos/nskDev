# -*- coding: utf-8 -*-
from django.db import models

class Country(models.Model):
	language_code = models.CharField(max_length=2)
	country_code = models.CharField(max_length=2)
	country = models.CharField(max_length=35)
	is_active = models.BooleanField(default=True)
	
	class Meta:
		unique_together = (("language_code", "country_code"),)
		verbose_name = "country"
		verbose_name_plural = "countries"
		ordering = ['country']

	def __unicode__(self):
		return self.country

class IDC(models.Model):
	idc = models.CharField(max_length=20, unique=True)

	class Meta:
		verbose_name = "identification"
		verbose_name_plural = "identifications"
		ordering = ['idc']

	def __unicode__(self):
		return self.idc

class DLic(models.Model):
	dLic = models.CharField(max_length=20, unique=True)

	class Meta:
		verbose_name = "driver's license"
		verbose_name_plural = "driver's licenses"
		ordering = ['dLic']

	def __unicode__(self):
		return self.dLic

class Relation(models.Model):
	relation = models.CharField(max_length=20)

	class Meta:
		verbose_name = "relation"
		verbose_name_plural = "relations"
		ordering = ['relation']

	def __unicode__(self):
		return self.relation

class WorkingStatus(models.Model):
	working_status = models.CharField(max_length=20)

	class Meta:
		verbose_name = "working status"
		verbose_name_plural = "working statuses"
		ordering = ['working_status']

	def __unicode__(self):
		return self.working_status

class Kind(models.Model):
	kind = models.CharField(max_length=20)

	class Meta:
		verbose_name = "kind"
		verbose_name_plural = "kinds"
		ordering = ['kind']
	
	def __unicode__(self):
		return self.kind

class Speciality(models.Model):
	speciality = models.CharField(max_length=20)
	
	class Meta:
		verbose_name = "Ειδικότητα"
		verbose_name_plural = "Ειδικότητες"
		ordering = ['speciality']

	def __unicode__(self):
		return self.speciality
	
class OrgPosition(models.Model):
	org_position = models.CharField(max_length=20)
	
	class Meta:
		verbose_name = "Θέση Εργασίας"
		verbose_name_plural = "Θέσεις Εργασίας"
		ordering = ['org_position']

	def __unicode__(self):
		return self.org_position
	
class Language(models.Model):
	language_code = models.CharField(max_length=2, unique=True)
	language_foreign_name = models.CharField(max_length=20)
	language = models.CharField(max_length=20)
	is_active = models.BooleanField(default=True)
	
	class Meta:
		verbose_name = "Γλώσσα"
		verbose_name_plural = "Γλώσσες"
		ordering = ['language']

	def __unicode__(self):
		return self.language
