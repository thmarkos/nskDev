from django.forms import ModelForm
from mysite.mgmt.models import Country, IDC, DLic, Relation, WorkingStatus, Owner, Kind

class CountryForm(ModelForm):
    class Meta:
        model = Country

class IDCForm(ModelForm):
    class Meta:
        model = IDC

class DLicForm(ModelForm):
    class Meta:
        model = DLic

class RelationForm(ModelForm):
    class Meta:
        model = Relation

class WorkingStatusForm(ModelForm):
    class Meta:
        model = WorkingStatus

class OwnerForm(ModelForm):
    class Meta:
        model = Owner

class KindForm(ModelForm):
    class Meta:
        model = Kind