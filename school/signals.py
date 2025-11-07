from .models import StudentAccount, StudentTerm
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg

@receiver(post_save, sender=StudentTerm)
def updating_avg(sender, instance, **kwargs):
    if instance.student_score != 0:
        lesson_grade = instance.term_lesson.grade_level
        instance.term_student.avg_update(lesson_grade)
        if instance.active_term:
            StudentTerm.objects.filter(id=instance.id).update(active_term=False)
