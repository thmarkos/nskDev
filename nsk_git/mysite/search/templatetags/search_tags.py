from django import template
from mysite.search.forms import SearchForm
import urllib

register = template.Library()

@register.inclusion_tag("tags/search_box.html")
def search_box(request):
		q = request.GET.get('q','')
		form = SearchForm({'q': q })
		return {'form': form }
			
@register.inclusion_tag('tags/pagination_links.html')
def pagination_links(request, paginator):
		raw_params = request.GET.copy()
		page = raw_params.get('page',1)
		p = paginator.page(page)
		try:
				del raw_params['page']
		except KeyError:
				pass
		#params = urllib.urlencode(raw_params)
		params = urllib.urlencode(dict([k, v.encode('utf-8')] for k, v in raw_params.items()))
		return {'request': request,'paginator': paginator,'p': p,'params': params }
	
@register.inclusion_tag("tags/search.html")
def search(request):
		q = request.GET.get('q','')
		form = SearchForm({'q': q })
		return {'form': form }
