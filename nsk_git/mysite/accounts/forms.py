from django.contrib.auth.forms import AuthenticationForm
from mysite.accounts.models import UserProfile
from mysite.hr.forms import DivErrorList
from django import forms

class AuthenticationFormCustom(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationFormCustom, self).__init__(*args, **kwargs)
        self.error_class = DivErrorList

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = {'employee_filter_preference'}                
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
                
