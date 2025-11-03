from django import template
import jdatetime
from ..models import StudentAccount

register = template.Library()

@register.simple_tag(name='time')
def now_time():
    tmp_date = jdatetime.datetime.now()
    date = tmp_date.strftime("%y/%m/%d ساعت: %H:%M")
    return date

# @register.simple_tag(name='top_grade_10_students')
# def top_grade_10_students():
#     grade_10_top_students = StudentAccount.objects.filter(grade_level='10').order_by('-avg_1')[:3]
    
#     return grade_10_top_students

# @register.simple_tag(name='top_grade_10_students')
# def top_grade_10_students():
#     grade_11_top_students = StudentAccount.objects.filter(grade_level='11').order_by('-avg_2')[:3]
    
#     return grade_11_top_students

# @register.simple_tag(name='top_grade_10_students')
# def top_grade_10_students():
#     grade_12_top_students = StudentAccount.objects.filter(grade_level='12').order_by('-avg_3')[:3]
#     return grade_12_top_students
