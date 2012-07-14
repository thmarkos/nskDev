from mysite.organization_chart.models import Chart
from mysite import settings

def mgmt(request):
	return {
		'site_name': settings.SITE_NAME,
		'meta_keywords': settings.META_KEYWORDS,
		'meta_description': settings.META_DESCRIPTION,
		'nodes': Chart.objects.all()
	}