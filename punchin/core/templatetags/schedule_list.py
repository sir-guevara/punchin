from django import template
from ..models import Schedule  # Import your Schedule model here
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter
def week_schedule_list(employee_id, date_range):
    print(date_range)
    start_date, end_date = date_range[0],date_range[-1]
    result = []
    current_date = start_date
    while current_date <= end_date:

        try:
            schedule = Schedule.objects.get(employee_id=employee_id, date=current_date)
        except ObjectDoesNotExist:
            schedule = None
        result.append({'date': current_date, 'schedule': schedule})
        current_date += timedelta(days=1)
    return result