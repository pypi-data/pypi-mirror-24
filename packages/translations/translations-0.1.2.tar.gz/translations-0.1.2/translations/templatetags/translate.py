from django import template
from django.utils import translation

register = template.Library()

@register.filter
def translate(model_instance, field_name, ):
    return model_instance.translate(field_name, translation.get_language())
