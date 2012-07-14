from mysite.search.models import SearchTerm
from mysite.hr.models import Employee
from django.db.models import Q

STRIP_WORDS = ['a','an','and','by','for','from','in','no','not','of','on','or','that','the','to','with']

# store the search text in the database
def store(request, q):
		# if search term is at least three chars long, store in db
		if len(q) > 2:
				term = SearchTerm()
				term.q = q
				term.ip_address = request.META.get('REMOTE_ADDR')
				term.user = None
				if request.user.is_authenticated():
						term.user = request.user
				term.save()
				
# get products matching the search text
def employees(search_text, sort, employee_filter):
		words = _prepare_words(search_text)
		employees = Employee.objects.all()
		results = {}
		results['employees'] = []
		# iterate through keywords
		if employee_filter is None:
			for word in words:
				employees = Employee.objects.filter(Q(id__icontains=word) |
				Q(name__icontains=word) |
				Q(father_name__icontains=word) |
				Q(surname__iexact=word)).order_by(sort)
				results['employees'] += employees
		else:
			for word in words:
				employees = Employee.objects.filter(is_active=employee_filter).filter(Q(id__icontains=word) |
				Q(name__icontains=word) |
				Q(father_name__icontains=word) |
				Q(surname__iexact=word)).order_by(sort)
				results['employees'] += employees
		return results
		
# strip out common words, limit to 5 words
def _prepare_words(search_text):
		words = search_text.split()
		for common in STRIP_WORDS:
				if common in words:
						words.remove(common)
		return words[0:5]