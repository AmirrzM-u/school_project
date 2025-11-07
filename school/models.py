from django.db import models
from django.contrib.auth.models import AbstractUser
from django_jalali.db import models as jmodels
from django.utils import timezone
from django.core.validators import RegexValidator, MaxValueValidator
from django.db.models import Q, CheckConstraint, UniqueConstraint
import jdatetime
from datetime import date
from django.db.models import Avg

class Classroom(models.Model):
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
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن',
                                    validators=[RegexValidator(
                                        regex=r"^09\d{9}$",
                                        message="شماره تلفن باید به صورت -> 09*********** باشد")],
                                    error_messages={
                                        'max_length':'شماره تلفن باید 11 رقم و با 09 شروع شود',
                                        'blank':'وارد کردن شمار تلفن الزامی است'})
    profile_pic = models.ImageField(upload_to=profile_img_upload_to, blank=True, null=True, verbose_name='عکس پروفایل')
    date_of_birth = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ تولد')
    class UserTypes(models.TextChoices):
        MANAGER = 'mng', 'مدیر'
        TEACHER = 'tch', 'معلم'
        STUDENT = 'std', 'دانش آموز'
        PARENT = 'prn', 'والد'
    user_type = models.CharField(max_length=3, choices=UserTypes, verbose_name='نوع کاربر')
    class Meta:
        verbose_name_plural = 'کاربران'
    
    @property
    def age(self):
        time = jdatetime.date.today().year
        if self.date_of_birth:
            birth = self.date_of_birth.year
        else:
            return None
        age = time - birth
        return age

    def __str__(self):
        return f"{self.first_name}-{self.last_name}-{self.user_type}"
    
class ManagerAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_account', verbose_name='کاربر')
    id_manager = models.PositiveSmallIntegerField(default=0, verbose_name='شناسه مدیر')

    class Meta:
        verbose_name_plural = 'اکانت مدیر'
        
    def __str__(self):
        return f"manager: {self.user.last_name}"

class StudentAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_account', verbose_name='کاربر')
    id_student = models.PositiveIntegerField(default=0, unique=True, verbose_name='شناسه دانش آموز')
    entry = jmodels.jDateField(default=timezone.now, verbose_name='سال روردی دانش آموز')
    avg_1 = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MaxValueValidator(20)], verbose_name='معدل سال اول')
    avg_2 = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MaxValueValidator(20)], verbose_name='معدل سال دوم')
    avg_3 = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MaxValueValidator(20)], verbose_name='معدل سال سوم')
    student_parent = models.OneToOneField('ParentAccount', on_delete=models.PROTECT, related_name='children', null=True, blank=True, verbose_name='والد دانش آموز')
    class GRADE_LEVELS(models.TextChoices):
        GRADE_10 = '10', 'Grade_10'
        GRADE_11 = '11', 'Grade_11'
        GRADE_12 = '12', 'Grade_12'
    grade_level = models.CharField(max_length=2, choices=GRADE_LEVELS, verbose_name='پایه دانش آموز')
    graduated = models.BooleanField(default=False, verbose_name='وضعیت فارغ التحصیلی')
    current_student = models.BooleanField(default=True, verbose_name='دانش آموز فعلی')
    student_class = models.ForeignKey('Classroom', on_delete=models.PROTECT, related_name='students', verbose_name='کلاس دانش آموز')
    student_term = models.ManyToManyField('TeacherAccount', through='StudentTerm', related_name='students',  through_fields=('term_student', 'term_teacher'), blank=True, verbose_name='درس های دانش آموز')
    extra_detail = models.CharField(max_length=500, verbose_name='اطلاعات اضافه', blank=True, null=True)
    
    @property
    def entry_year(self):
        if self.entry:
            shamsi_date = jdatetime.date.fromgregorian(date=self.entry)
            return shamsi_date.year
        return None
    
    def avg_update(self, grade):
        avg_data = self.term_student.filter(term_lesson__grade_level=grade).exclude(student_score=0).aggregate(avg=Avg('student_score'))
        grade_avg_map = {
            '10':'avg_1',
            '11':'avg_2',
            '12':'avg_3',
        }
        avg_field = grade_avg_map.get(str(grade))
        setattr(self, avg_field, avg_data['avg'])
        self.save(update_fields=[avg_field])
    
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
        verbose_name_plural = 'اکانت دانش آموزان'
    
    def __str__(self):
        return f"std:{self.user.first_name}-{self.user.last_name}"
    
class ParentAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_account', verbose_name='کاربر')
    extra_detail = models.CharField(max_length=500, verbose_name='اطلاعات اضافه', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'اکانت والدین'

    def __str__(self):
        return f"Mr/Ms {self.user.last_name}"

class TeacherAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_account', verbose_name='کاربر')
    id_teacher = models.PositiveSmallIntegerField(default=0, verbose_name='شناسه معلم')
    extra_detail = models.CharField(max_length=500, verbose_name='اطلاعات اضافه', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'اکانت معلم ها'
  
    def __str__(self):
        return f"teacher: {self.user.last_name}"

class StudentTerm(models.Model):
    term_lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='student_term', verbose_name='درس')
    term_teacher = models.ForeignKey(TeacherAccount, on_delete=models.CASCADE, related_name='term_teacher', verbose_name='معلم این درس')
    term_student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE, related_name='term_student', verbose_name='دانش آموز این درس')
    student_score = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MaxValueValidator(20)], verbose_name='نمره دانش آموز')
    term_time = jmodels.jDateField(default=timezone.now, verbose_name='تاریخ')
    active_term = models.BooleanField(default=True, verbose_name='فعال بودن ترم')
    update = jmodels.jDateField(auto_now=True, verbose_name='اخرین بروزرسانی')
    
    objects = jmodels.jManager()

    @property
    def term_year(self):
        year = jdatetime.date.fromgregorian(date=self.term_time).year
        return year

    class Meta:
        ordering = ['term_teacher']
        indexes = [
            models.Index(fields=['term_teacher', 'term_lesson'])
        ]
        verbose_name_plural = 'سال تحصیلی دانش آموزان'

    def __str__(self):
        return f"term: {self.term_lesson}-{self.term_teacher.user.last_name}"
    
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

def school_news_title_img_upload_to(instance, filename):
    title = instance.title
    return f"news_imgs/{title}/{filename}"
def school_news_img_upload_to(instance, filename):
    title = instance.title
    return f"news_imgs/{title}-description_photos/{filename}"

class SchoolNews(models.Model):
    title = models.CharField(max_length=100, verbose_name='موضوع')
    title_image = models.ImageField(upload_to=school_news_title_img_upload_to)
    description = models.CharField(max_length=1000, verbose_name='توضیحات')
    date = jmodels.jDateTimeField(default=timezone.now, verbose_name='تاریخ')

    class Meta:
        ordering = ['date']
        indexes = [
            models.Index(fields=['date'])
        ]
        verbose_name_plural = 'اخبار دبیرستان'

    def __str__(self):
        return f"{self.title}"
    

def school_news_img_description_upload_to(instance, filename):
    title = instance.title
    return f"new_imgs/{title}-description_photos/{filename}"

class ImageModel(models.Model):
    title = models.CharField(max_length=100, verbose_name='توضیحات عکس')
    news = models.ForeignKey(SchoolNews, on_delete=models.CASCADE, related_name='description_image', verbose_name='خبر')
    image = models.ImageField(upload_to=school_news_img_description_upload_to)

class Ticket(models.Model):
    parent = models.ForeignKey(ParentAccount, on_delete=models.CASCADE, related_name='parent_tickets', verbose_name='والد')
    teacher = models.ForeignKey(TeacherAccount, on_delete=models.CASCADE, related_name='teacher_tickets', verbose_name='معلم')
    title = models.CharField(max_length=200, verbose_name='موضوع')
    description = models.CharField(max_length=1000, verbose_name='توضیحات')
    class Status(models.TextChoices):
        CHECKED = 'true', 'Checked'
        NOT_CHECKED = 'false', "Not checked"
    status = models.CharField(max_length=5, choices=Status, default=Status.NOT_CHECKED, verbose_name='وضعیت')
    response = models.CharField(max_length=1000, verbose_name='پاسخ معلم', blank=True, null=True)
    
    class Meta:
        ordering = ['status']
        indexes = [
            models.Index(fields=['status'])
        ]
        verbose_name_plural = 'پیام'

    def __str__(self):
        return f"parent: {self.parent.user.last_name}-{self.title} to: {self.teacher.user.last_name}"




