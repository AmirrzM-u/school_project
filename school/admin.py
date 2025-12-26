from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django_jalali.admin.filters import JDateFieldListFilter

# Creating accounts inlines for users and different user_types
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

# registering User model and creating a panel for it
@admin.register(User)
class UserPanelAdmin(UserAdmin):
    # Proper description for user last_name, first_name and email for list_displays in persian
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

    # adding extra fields from AbstractUser in models.py as user info
    fieldsets = list(UserAdmin.fieldsets) + [
        (
            'user info', {
                'fields':(
                    'phone_number', 'date_of_birth', 'user_type'
                )
            }
        )
    ]
    # Adding Inlines
    inlines = [ManagerAccountInline, StudentAccountInline, TeacherAccountInline, ParentAccountInline]

    # Overriding the get_inline_instances so each user can will be shown with it's own account after being created
    def get_inline_instances(self, request, instance=None):
        '''
        By overriding get_inline_instances,
        we ensure that the correct account inline is returned based on the users user_type, 
        and that all inlines are shown when creating a new user
        '''
        inline_instance = []
        inline_map = {
            'mng':ManagerAccountInline,
            'std':StudentAccountInline,
            'tch':TeacherAccountInline,
            'prn':ParentAccountInline,
        }
        if instance:
            user_type = getattr(instance, 'user_type', None)
            if user_type:
                inline = inline_map.get(user_type)
                inline_instance.append(inline(self.model, self.admin_site))
                return inline_instance

        inline_instance = [inline(self.model, self.admin_site) for inline in self.inlines]
        return inline_instance


# registering ParentAccount model and creating a panel for it
@admin.register(ParentAccount)
class ParentPanelAdmin(admin.ModelAdmin):
    list_display = ['user__last_name']
    search_fields = ['user__first_name', 'user__last_name']
    readonly_fields = ['children']

    # Adding childrens for parents and Proper description for it in persian
    @admin.display(description='فرزندان')
    def children(self, instance):
        childrens = instance.children.all()
        return list(f"{children.user.first_name}-{children.user.last_name}" for children in childrens)

# registering TeacherAccount model and creating a panel for it
@admin.register(TeacherAccount)
class TeacherPanelAdmin(admin.ModelAdmin):
    list_display = ['user__last_name']
    search_fields = ['user__first_name', 'user__last_name']
    
    # Adding students for teachers and Proper description for it in persian
    @admin.display(description='دانش آموزان', empty_value='بدون دانش آموز')
    def students_list(self, instance):
      students = instance.students.filter(term_student__active_term=True)
      return str([student.user.last_name for student in students])
    readonly_fields = ['students_list']

# registering StudentAccount model and creating a panel for it
@admin.register(StudentAccount)
class StudentPanelAdmin(admin.ModelAdmin):

    # Adding entry_year for students and Proper description for it in persian
    @admin.display(description='سال ورودی')
    def entry_year(self, instance):
        year = instance.entry_year
        return year
    
    # Adding user_last_name for students and Proper description for it in persian
    @admin.display(description='نام خوانوادگی')
    def user_last_name(self, instance):
        user_last_name = instance.user.last_name
        return user_last_name
    
    list_display = ['user_last_name', 'grade_level', 'entry_year', 'current_student', 'graduated']
    ordering = ['current_student', '-graduated', 'entry', 'grade_level', 'student_class']
    list_filter = [('entry', JDateFieldListFilter), 'student_class', 'grade_level']
    search_fields = ['user__first_name', 'user__last_name', 'grade_level']

# registering Classroom model and creating a panel for it
@admin.register(Classroom)
class ClassroomPanelAdmin(admin.ModelAdmin):
    list_display = ['class_number', 'students_number']
    readonly_fields = ['class_students']

    # Adding students for classrooms and Proper description for it in persian
    @admin.display(description='دانش آموزان کلاس')
    def class_students(self, instance):
        students = instance.students.filter(current_student=True, graduated=False)
        return list(f"{student.user.first_name} {student.user.last_name}" for student in students)

    # Adding students_number for classrooms and Proper description for it in persian
    @admin.display(description='تعداد دانش آموز', empty_value='بدون دانش آموز')
    def students_number(self, instance):
        return instance.students.filter(current_student=True, graduated=False).count()
    
    students_number.short_description = 'تعداد دانش آموزان'

# registering Lesson model and creating a panel for it
@admin.register(Lesson)
class LessonPanelAdmin(admin.ModelAdmin):
    list_display = ['title', 'grade_level', 'lesson_times']

# registering StudentTerm model and creating a panel for it
@admin.register(StudentTerm)
class TermPanelAdmin(admin.ModelAdmin):
    
    # Adding term_year for students term and Proper description for it in persian
    @admin.display(description='سال')
    def term_year(self, instance):
        term_year = instance.term_time.year
        return term_year
    
    list_display = ['term_student', 'term_lesson', 'term_teacher', 'student_score', 'term_year', 'active_term']
    autocomplete_fields = ['term_student']
    ordering = ['term_time', 'term_lesson', 'term_teacher', 'student_score', 'active_term']
    list_filter = ['term_lesson', 'term_teacher', ('term_time', JDateFieldListFilter), 'active_term']
    search_fields = ['term_student__user__first_name', 'term_student__user__last_name', 'term_lesson__title', 'term_teacher__user__last_name']

# registering ManagerAccount model and creating a panel for it
@admin.register(ManagerAccount)
class ManagerPanelAdmin(admin.ModelAdmin):
    list_display = ['id_manager']

# registering SchoolNews model and creating a panel for it
@admin.register(SchoolNews)
class SchoolNewsPanelAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [ImageInline]

# registering Ticket model and creating a panel for it
@admin.register(Ticket)
class TicketPanelAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_editable = ['status']
