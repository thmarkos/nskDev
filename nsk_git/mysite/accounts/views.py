# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.contrib.auth.models import User
from mysite.accounts.forms import UserProfileForm
from mysite.accounts.models import UserProfile

@login_required
def my_account(request, template_name="registration/my_account.html"):
		title = 'Ο Λογαριασμός μου'
		name = request.user.username
		return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def change_preference(request):
	#u = User.objects.get(id=1)
	#UserProfile.objects.get_or_create(user = u)
	if request.method == 'GET':
		user_profile = UserProfile.objects.get(id=request.user.get_profile().id)
		form = UserProfileForm(request.GET, instance=user_profile)
		if form.is_valid():
			form.save()
	return_url = request.GET.get('return_url', '')
	return HttpResponseRedirect(return_url)			

