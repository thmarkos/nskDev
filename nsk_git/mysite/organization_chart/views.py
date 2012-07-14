from django.shortcuts import render_to_response
from django.template import RequestContext
from mysite.organization_chart.models import Chart
from mysite.organization_chart import script

def show_chart(request, template_name="organization_chart/chart.html"):
    #script.create_chart_structure()
    nodes = Chart.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
