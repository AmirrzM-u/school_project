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
    class UserTypes(models.TextChoices):
        TEACHER = 'tch', 'teacher'
        STUDENT = 'std', 'student'
        PARENT = 'prn', 'parent'
    user_type = models.CharField(max_length=3, choices=UserTypes, verbose_name='نوع کاربر')
    class Meta:
        verbose_name_plural = 'کاربران'

class StudentAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_account', verbose_name='کاربر')
    entry = jmodels.jDateField(default=timezone.now, verbose_name='سال روردی دانش آموز')
    avg_1 = models.PositiveIntegerField(default=0, verbose_name='معدل سال اول')
    avg_2 = models.PositiveIntegerField(default=0, verbose_name='معدل سال دوم')
    avg_3 = models.PositiveIntegerField(default=0, verbose_name='معدل سال سوم')
    student_parent = models.ForeignKey('ParentAccount', on_delete=models.CASCADE, related_name='children', verbose_name='والد دانش آموز')
    class GRADE_LEVELS(models.TextChoices):
        GRADE_10 = '10', 'Grade_10'
        GRADE_11 = '11', 'Grade_11'
        GRADE_12 = '12', 'Grade_12'
    grade_level = models.CharField(max_length=2, choices=GRADE_LEVELS, verbose_name='پایه دانش آموز')
    graduated = models.BooleanField(default=False, verbose_name='وضعیت فارغ التحصیلی')
    current_student = models.BooleanField(default=True, verbose_name='دانش آموز فعلی')
    student_class = models.ForeignKey('Class', on_delete=models.PROTECT, related_name='students', verbose_name='کلاس دانش آموز')
    student_term = models.ManyToManyField('TeacherAccount', through='StudentTerm', related_name='students',  through_fields=('lesson_student', 'lesson_teacher'), blank=True, verbose_name='درس های دانش آموز')
    extra_detail = models.CharField(verbose_name='اطلاعات اضافه', blank=True, null=True)
    
    class ActiveStudentManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(current_student=True, graduated=False)
    
    objects = jmodels.jManager()
    active = ActiveStudentManager()

    class Meta:
        ordering = ['entry'] 
        indexes = [
            models.Index(fields=['entry', 'user', 'grade_level'])
        ]
        verbose_name_plural = 'اکانت دانش آموز'
    
    def __str__(self):
        return f"std:{self.user.first_name}-{self.user.last_name}"
    
class ParentAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_account', verbose_name='کاربر')
    extra_detail = models.CharField(verbose_name='اطلاعات اضافه', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'والدین'
    def __str__(self):
        return f"Mr/Ms {self.user.last_name}"

class TeacherAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_account', verbose_name='کاربر')

    class Meta:
        verbose_name_plural = 'معلم'
    def __str__(self):
        return f"teacher: {self.user.last_name}"

class StudentTerm(models.Model):
    term_lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='student_term', verbose_name='درس')
    lesson_teacher = models.ForeignKey(TeacherAccount, on_delete=models.CASCADE, related_name='lessons', verbose_name='معلم این درس')
    lesson_student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE, related_name='lessons', verbose_name='دانش آموز این درس')
    student_score = models.PositiveSmallIntegerField(default=0, verbose_name='نمره دانش آموز')
    term_time = jmodels.jDateField(default=timezone.now, verbose_name='تاریخ')
    update = jmodels.jDateField(auto_now=True, verbose_name='اخرین بروزرسانی')

    objects = jmodels.jManager()

    class Meta:
        ordering = ['lesson_teacher']
        indexes = [
            models.Index(fields=['lesson_teacher', 'term_lesson'])
        ]
        verbose_name_plural = 'سال تحصیلی دانش آموز'
    def __str__(self):
        return f"lesson: {self.title}"
    
class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='نام درس')
    class GRADE_LEVELS(models.TextChoices):
        GRADE_10 = '10', 'Grade_10'
        GRADE_11 = '11', 'Grade_11'
        GRADE_12 = '12', 'Grade_12'
    grade_level = models.CharField(max_length=2, choices=GRADE_LEVELS, verbose_name='پایه درس')
    lesson_times = models.CharField(max_length=500, verbose_name='ساعت و روز های درس')
    update = jmodels.jDateField(auto_now=True, verbose_name='اخرین بروزرسانی')

    objects = jmodels.jManager()

    class Meta:
        verbose_name_plural = 'درس'
    def __str__(self):
        return f"lesson: {self.title}"
            





