from django import template
import jdatetime

register = template.Library()

@register.simple_tag(name='time')
def now_time():
    tmp_date = jdatetime.datetime.now()
    date = tmp_date.strftime("%y/%m/%d ساعت: %H:%M")
    return date