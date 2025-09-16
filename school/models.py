from django.db import models
from django.contrib.auth.models import AbstractUser
from django_jalali.db import models as jmodels
from django.utils import timezone

class Class(models.Model):
    class_number = models.CharField(max_length=3, verbose_name='شماره کلاس')
    class Meta:
        verbose_name_plural = 'کلاس'
    def __str__(self):
        return f"class: {self.class_number}"

def profile_img_upload_to(instance, filename):
    user_first_name = instance.first_name
    user_last_name = instance.last_name
    return f"profile_img/{user_first_name}-{user_last_name}/{filename}"

class User(AbstractUser):
    phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن')
    profile_pic = models.ImageField(upload_to=profile_img_upload_to, blank=True, null=True, verbose_name='عکس پروفایل')
    date_of_birth = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ تولد')
    age = models.CharField(max_length=2, blank=True, null=True, verbose_name='سن')

class StudentAccount(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_account', verbose_name='دانش آموز')
    entry = jmodels.jDateField(default=timezone.now, verbose_name='سال روردی دانش آموز')
    avg_1 = models.PositiveIntegerField(default=0, verbose_name='معدل سال اول')
    avg_2 = models.PositiveIntegerField(default=0, verbose_name='معدل سال دوم')
    avg_3 = models.PositiveIntegerField(default=0, verbose_name='معدل سال سوم')
    class GRADE_LEVELS(models.TextChoices):
        GRADE_10 = '10', 'Grade_10'
        GRADE_11 = '11', 'Grade_11'
        GRADE_12 = '12', 'Grade_12'
    grade_level = models.CharField(max_length=2, choices=GRADE_LEVELS, verbose_name='پایه دانش آموز')
    graduated = models.BooleanField(default=False, verbose_name='وضعیت فارغ التحصیلی')
    current_student = models.BooleanField(default=True, verbose_name='دانش آموز فعلی')
    student_class = models.ForeignKey('Class', on_delete=models.PROTECT, related_name='students', verbose_name='کلاس دانش آموز')
    student_teachers = models.ManyToManyField('TeacherAccount',  related_name='students', verbose_name='معلم های دانش آموز')
    student_lessons = models.ManyToManyField('Lesson', related_name='students')
    extra_detail = models.CharField(verbose_name='اطلاعات اضافه')

    class Meta:
        ordering = ['-entry'] 
        indexes = [
            models.Index(fields=['-student'])
        ]
        verbose_name_plural = 'اکانت دانش آموز'
    
    def __str__(self):
        return f"student: {self.student.first_name} {self.student.last_name}"
    
class ParentAccount(models.Model):
    parent = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_account', verbose_name='والدین')
    parent_of = models.OneToOneField(StudentAccount, on_delete=models.CASCADE, related_name='parent')
    extra_detail = models.CharField(verbose_name='اطلاعات اضافه')
    
    class Meta:
        verbose_name_plural = 'والدین'
    def __str__(self):
        return f"parent Mr/Ms {self.parent.last_name}"

class TeacherAccount(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_account')
    lessons = models.ManyToManyField('Lesson', related_name='teachers')

    class Meta:
        verbose_name_plural = 'معلم'
    def __str__(self):
        return f"teacher: {self.teacher.last_name}"

class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='نام درس')
    class GRADE_LEVELS(models.TextChoices):
        GRADE_10 = '10', 'Grade_10'
        GRADE_11 = '11', 'Grade_11'
        GRADE_12 = '12', 'Grade_12'
    grade_level = models.CharField(max_length=2, choices=GRADE_LEVELS, verbose_name='پایه درس')

    class Meta:
        verbose_name_plural = 'درس'
    def __str__(self):
        return f"lesson: {self.title}"




