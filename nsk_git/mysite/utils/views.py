from mysite.utils.models import Genre
from django.shortcuts import render_to_response
from django.template import RequestContext

def show_genres(request, template_name = "utils/genres.html"):
		nodes = Genre.objects.all()
		return render_to_response(template_name, locals(), context_instance=RequestContext(request))
