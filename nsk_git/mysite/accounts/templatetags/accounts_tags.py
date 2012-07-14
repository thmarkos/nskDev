from django import template
from mysite.accounts.forms import UserProfileForm

register = template.Library()

@register.inclusion_tag("tags/select_employee_filter_preference.html")
def select_employee_filter(request):
		form = UserProfileForm(initial={'employee_filter_preference': request.user.get_profile().employee_filter_preference})
		return {'form': form , 'request': request}
			