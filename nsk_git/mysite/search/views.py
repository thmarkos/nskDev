# -*- coding: utf-8 -*-
from mysite.hr.models import Employee
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from mysite.search import search
from mysite import settings
from django.contrib.auth.decorators import login_required
from mysite.organization_chart.models import Chart
import urllib

@login_required
def results(request, template_name="search/results.html"):	
	# get current search phrase
	q = request.GET.get('q', '')
	# get current page number. Set to 1 is missing or invalid
	try:
		page = int(request.GET.get('page', 1))
	except ValueError:
		page = 1
	# retrieve the matching products
	matching = search.employees(q).get('employees')
	# generate the pagintor object
	paginator = Paginator(matching, settings.PRODUCTS_PER_PAGE)
	try:
		results = paginator.page(page).object_list
	except (InvalidPage, EmptyPage):
		results = paginator.page(1).object_list
	# store the search
	search.store(request, q)
	# the usual
	page_title = 'Search Results for: ' + q
	return render_to_response(template_name, locals(), context_instance=RequestContext(request))
	
@login_required
def search_results(request, template_name="search/search_results.html"):
	q = request.GET.get('q', '')	
	q_url_encoded = urllib.quote_plus(q.encode('utf8'))
	
	title = 'Αποτελέσματα Αναζήτησης για %s' % (q,)
	
	sort = Employee._meta.ordering[0] #@UndefinedVariable
	#sort = 'name'  #default sort
	if 'sort' in request.GET:
		sort = request.GET['sort']
		
	pref = request.user.get_profile().employee_filter_preference
	employee_filter = None
	if pref == 'ACTIVE':
		employee_filter = True
		matching = search.employees(q, sort, employee_filter).get('employees')
	if pref == 'INACTIVE':
		employee_filter = False
		matching = search.employees(q, sort, employee_filter).get('employees')
	if pref == 'ALL':
		matching = search.employees(q, sort, employee_filter).get('employees')
	
	#matching = search.employees(q).get('employees')
	nodes = Chart.objects.all()
	return render_to_response(template_name, locals(), context_instance=RequestContext(request))
