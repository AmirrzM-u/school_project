from .models import User, StudentTerm
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg
from django.contrib.auth.models import Group
from django.db import transaction

@receiver(post_save, sender=StudentTerm)
def updating_avg(sender, instance, **kwargs):
    if instance.student_score != 0:
        lesson_grade = instance.term_lesson.grade_level
        instance.term_student.avg_update(lesson_grade)
        if instance.active_term:
            StudentTerm.objects.filter(id=instance.id).update(active_term=False)

@receiver(post_save, sender=User)
def assigning_users_to_groups(sender, instance, created, **kwargs):
    if not created:
        group_map = {
            'tch': 'Teachers',
            'prn': 'Parents'
        }

        group_name = group_map[instance.user_type]
        if not group_name:
            return
        
        group = Group.objects.get(name=group_name)
        transaction.on_commit(lambda: instance.groups.add(group))

            

