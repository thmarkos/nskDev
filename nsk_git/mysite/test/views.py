from django.views.decorators.csrf import csrf_exempt
#from django.utils import simplejson
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from mysite.utils.models import Genre, Tree

def test(request, template_name="test/test.html"):
    trees = Tree.objects.all()
    #template = "mgmt/test.html"
    #html = render_to_string(template, {'request': request })
    #response = simplejson.dumps({'success':'True', 'html': html})
    #return HttpResponse(response, content_type='application/json; charset=utf-8')
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@csrf_exempt
def testin(request, template_name="test/testin.html"):
    data = request.POST.get('data')
    tree = Tree()
    tree.json_string = request.POST.get('data')
    tree.save()
    #template = "mgmt/testin.html"
    #html = render_to_string(template, {'request': request })
    #response = simplejson.dumps({'success':'True', 'data': data})
    #return HttpResponse(response, content_type='application/json; charset=utf-8')
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
    
def testout(request):
    tree = Tree.objects.get(id = 12)
    #template = "mgmt/test.html"
    #html = render_to_string(template, {'request': request })
    #response = simplejson.dumps({'success':'True', 'tree': tree})
    return HttpResponse(tree, content_type='application/json; charset=utf-8')

@csrf_exempt
def testoutf(request):
    #tree = Tree.objects.get(id = 15)
    template = "test/testoutf.html"
    nodes = Genre.objects.all()
    html = render_to_string(template, {'nodes': nodes })
    html = html.replace(',]',']')
    #html = html.decode('ascii', 'ignore')
    #urllib.urlencode(html)
    #response = simplejson.dumps({html}, ensure_ascii=True)
    return HttpResponse(html, content_type='application/json; charset=utf-8')
