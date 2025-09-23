from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

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

@admin.register(User)
class UserPanelAdmin(UserAdmin):
    list_display = ['last_name', 'first_name', 'email', 'user_type']
    ordering = ['user_type']
    fieldsets = list(UserAdmin.fieldsets) + [
        (
            'user info', {
                'fields':(
                    'phone_number', 'date_of_birth', 'age', 'user_type'
                )
            }
        )
    ]
    inlines = [StudentAccountInline, TeacherAccountInline, ParentAccountInline]

    def get_inline_instances(self, request, obj=None):  
        inline_instances = []

        target_type = None
        if obj is not None:
            target_type = getattr(obj, 'user_type', None)
        else:
            target_type = request.GET.get('user_type')

        for inline_class in self.inlines:
            should_include = False

            if target_type:
                if inline_class is StudentAccountInline and target_type =='std':
                    should_include = True
                elif inline_class is TeacherAccountInline and target_type == 'tch':
                    should_include = True
                elif inline_class is ParentAccountInline and target_type == 'prn':
                    should_include = True

            if should_include:
                inline = inline_class(self.model, self.admin_site)
                inline_instances.append(inline)

        return inline_instances

@admin.register(ParentAccount)
class ParentPanelAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['children']

    @admin.display(description='فرزندان')
    def chidren(self, instance):
        childrens = instance.children.all()
        return list(f"{children.user.first_name}-{children.user.last_name}" for children in childrens)

@admin.register(TeacherAccount)
class TeacherPanelAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['students']

    @admin.display(description='دانش آموزان')
    def students(self, instance):
        students = instance.term.term_student.all()
        return list(f"{student.user.first_name}-{student.user.last_name}" for student in students)
 

@admin.register(StudentAccount)
class StudentPanelAdmin(admin.ModelAdmin):
    list_display = ['user', 'grade_level', 'entry_year', 'current_student', 'graduated']

    @admin.display(description='سال ورودی')
    def entry_year(self, instance):
        year = instance.entry.year
        return str(year)


@admin.register(Class)
class ClassPanleAdmin(admin.ModelAdmin):
    list_display = ['class_number', 'students_number']
    # fields = ['class_number', 'students_number']
    readonly_fields = ['class_students']

    @admin.display(description='دانش آموزان کلاس')
    def class_students(self, instance):
        students = instance.students.filter(current_student=True, graduated=False)
        return list(f"{student.user.first_name} {student.user.last_name}" for student in students)

    @admin.display(empty_value='بدون دانش آموز')
    def students_number(self, obj):
        return obj.students.all().count()
    
    students_number.short_description = 'تعداد دانش آموزان'

@admin.register(Lesson)
class LessonPanelAdmin(admin.ModelAdmin):
    list_display = ['title', 'grade_level']

# @admin.register(StudentTerm)
# class TermPanelAdmin(admin.ModelAdmin):
#     pass
