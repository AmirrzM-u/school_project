from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django_jalali.admin.filters import JDateFieldListFilter


class ManagerAccountInline(admin.StackedInline):
    model = ManagerAccount
    extra = 0
    max_num = 1

class StudentAccountInline(admin.StackedInline):
    model = StudentAccount
    extra = 0
    max_num = 1

class TeacherAccountInline(admin.StackedInline):
    model = TeacherAccount
    extra = 0
    max_num = 1

class ParentAccountInline(admin.StackedInline):
    model = ParentAccount
    extra = 0
    max_num = 1

class ImageInline(admin.StackedInline):
    model = ImageModel
    extra = 1

@admin.register(User)
class UserPanelAdmin(UserAdmin):
    @admin.display(description='نام خانوادگی')
    def user_last_name(self, instance):
        return instance.last_name
    @admin.display(description='نام')
    def user_first_name(self, instance):
        return instance.first_name
    @admin.display(description='ایمیل')
    def user_email(self, instance):
        return instance.email

    list_display = ['user_last_name', 'user_first_name', 'user_email', 'user_type']
    search_fields = ['last_name', 'first_name', 'email', 'user_type']
    list_filter = ['user_type']
    ordering = ['user_type']
    fieldsets = list(UserAdmin.fieldsets) + [
        (
            'user info', {
                'fields':(
                    'phone_number', 'date_of_birth', 'user_type'
                )
            }
        )
    ]
    inlines = [ManagerAccountInline, StudentAccountInline, TeacherAccountInline, ParentAccountInline]

    def get_inline_instances(self, request, instance=None):
        inline_instance = []
        inline_map = {
            'mng':ManagerAccountInline,
            'std':StudentAccountInline,
            'tch':TeacherAccountInline,
            'prn':ParentAccountInline,
        }
        if instance:
            user_type = getattr(instance, 'user_type', None)
            print("user_type is: ", user_type)
            if user_type:
                print("you are here")
                inline = inline_map.get(user_type)
                inline_instance.append(inline(self.model, self.admin_site))
                return inline_instance

        print("you are there")
        inline_instance = [inline(self.model, self.admin_site) for inline in self.inlines]
        return inline_instance



@admin.register(ParentAccount)
class ParentPanelAdmin(admin.ModelAdmin):
    list_display = ['user__last_name']
    search_fields = ['user__first_name', 'user__last_name']
    readonly_fields = ['children']

    @admin.display(description='فرزندان')
    def children(self, instance):
        childrens = instance.children.all()
        return list(f"{children.user.first_name}-{children.user.last_name}" for children in childrens)

@admin.register(TeacherAccount)
class TeacherPanelAdmin(admin.ModelAdmin):
    list_display = ['user__last_name']
    search_fields = ['user__first_name', 'user__last_name']
    
    @admin.display(description='دانش آموزان', empty_value='بدون دانش آموز')
    def students_list(self, instance):
      students = instance.students.filter(term_student__active_term=True)
      return str([student.user.last_name for student in students])
    readonly_fields = ['students_list']

@admin.register(StudentAccount)
class StudentPanelAdmin(admin.ModelAdmin):
    @admin.display(description='سال ورودی')
    def entry_year(self, instance):
        year = instance.entry_year
        return year
    @admin.display(description='نام خوانوادگی')
    def user_last_name(self, instance):
        user_last_name = instance.user.last_name
        return user_last_name
    
    list_display = ['user_last_name', 'grade_level', 'entry_year', 'current_student', 'graduated']
    ordering = ['current_student', '-graduated', 'entry', 'grade_level', 'student_class']
    list_filter = [('entry', JDateFieldListFilter), 'student_class', 'grade_level']
    search_fields = ['user__first_name', 'user_last_name', 'grade_level']

@admin.register(Classroom)
class ClassroomPanelAdmin(admin.ModelAdmin):
    list_display = ['class_number', 'students_number']
    readonly_fields = ['class_students']

    @admin.display(description='دانش آموزان کلاس')
    def class_students(self, instance):
        students = instance.students.filter(current_student=True, graduated=False)
        return list(f"{student.user.first_name} {student.user.last_name}" for student in students)

    @admin.display(description='تعداد دانش آموز', empty_value='بدون دانش آموز')
    def students_number(self, instance):
        return instance.students.filter(current_student=True, graduated=False).count()
    
    students_number.short_description = 'تعداد دانش آموزان'

@admin.register(Lesson)
class LessonPanelAdmin(admin.ModelAdmin):
    list_display = ['title', 'grade_level', 'lesson_times']

@admin.register(StudentTerm)
class TermPanelAdmin(admin.ModelAdmin):
    
    @admin.display(description='سال')
    def term_year(self, instance):
        term_year = instance.term_time.year
        return term_year
    
    list_display = ['term_student', 'term_lesson', 'term_teacher', 'student_score', 'term_year', 'active_term']
    autocomplete_fields = ['term_student']
    ordering = ['term_time', 'term_lesson', 'term_teacher', 'student_score', 'active_term']
    list_filter = ['term_lesson', 'term_teacher', ('term_time', JDateFieldListFilter), 'active_term']
    search_fields = ['term_student__user__first_name', 'term_student__user__last_name', 'term_lesson__title', 'term_teacher__user__last_name']

@admin.register(ManagerAccount)
class ManagerPanelAdmin(admin.ModelAdmin):
    list_display = ['id_manager']

@admin.register(SchoolNews)
class SchoolNewsPanelAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [ImageInline]

@admin.register(Ticket)
class TicketPanelAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_editable = ['status']
