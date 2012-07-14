from django import template
from mysite import settings

register = template.Library()

@register.filter
def verbose_name(obj, field):
    return obj.get_verbose_name(field)

@register.filter
def yes_no(obj):
    if obj == True:
        return "<img src=\"%sicon-yes.gif\" alt=\"True\" />" % (settings.STATIC_URL,)
    if obj == False:
        return "<img src=\"%sicon-no.gif\" alt= \"False\" />" % (settings.STATIC_URL,)  
    if obj is None:
        return "<img src=\"%sicon-no.gif\" alt= \"False\" />" % (settings.STATIC_URL,)   
    return obj

@register.filter
def sub_none(obj):
    if obj is None:
        return "<img src=\"%sicon-no.gif\" alt= \"False\" />" % (settings.STATIC_URL,)   
    return obj