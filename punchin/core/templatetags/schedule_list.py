from django import template
from ..models import Schedule  # Import your Schedule model here
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

