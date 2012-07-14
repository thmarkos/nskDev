from mysite.search.models import SearchTerm
from django import forms

class SearchForm(forms.ModelForm):
	class Meta:
		model = SearchTerm
		widgets = {
			'q': forms.TextInput(attrs={'class': 'ym-searchfield'}),
		}		
				
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		default_text = 'Search'
		self.fields['q'].widget.attrs['value'] = default_text
		self.fields['q'].widget.attrs['onfocus'] = "if (this.value=='" + default_text + "')this.value = ''"
				
	include = ('q',)