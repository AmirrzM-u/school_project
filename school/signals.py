from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=StudentTerm)
def deactivate_term(sender, instance, **kwargs):
    if instance.student_score and instance.active_term:
        StudentTerm.objects.filter(id=instance.id).update(active_term=False)