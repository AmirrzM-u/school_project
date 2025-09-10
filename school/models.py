from django.db import models
from django.contrib.auth.models import AbstractUser
from django_jalali.db import models as jmodels
from django.utils import timezone

def profile_img_upload_to(instance, filename):
    user_first_name = instance.first_name
    user_last_name = instance.last_name
    return f"profile_img/{user_first_name}-{user_last_name}/{filename}"

class User(AbstractUser):
    phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن')
    profile_pic = models.ImageField(upload_to=profile_img_upload_to, blank=True, null=True, verbose_name='عکس پروفایل')
    date_of_birth = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ تولد')
    age = models.CharField(max_length=2, blank=True, null=True, verbose_name='سن')

class StudentAccount():
    entry = jmodels.jDateField(default=timezone.now, verbose_name='سال روردی')
    avg_1 = models.PositiveIntegerField(default=0)
    avg_2 = models.PositiveIntegerField(default=0)
    avg_3 = models.PositiveIntegerField(default=0)
    # class_number =
    class GRADE_LEVELS(models.TextChoices):
        GRADE_10 = '10', 'Grade_10'
        GRADE_11 = '11', 'Grade_11'
        GRADE_12 = '12', 'Grade_12'

    grade_level = models.CharField(max_length=2, choices=GRADE_LEVELS)