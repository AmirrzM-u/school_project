from django import forms
from .models import *
from django.contrib.auth import authenticate

# Base sign-in form that provides authentication logic for all user types.
class BaseSigninForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='نام کاربری')
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput, label='رمز عبور')

    # Auth function to check the username and password and return the user if it existed 
    def authenticate_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                return user
            else:
                raise forms.ValidationError('نام کاربری یا رمز عبور اشتباه است')

# Sign in form for students
class StudentSigninForm(BaseSigninForm):
    student_id = forms.IntegerField(required=True, label='شناسه دانش آموز')

    # Overriding the clean method for checking the student id
    def clean(self):
        cd = super().clean()
        student_id = cd.get('student_id')

        if student_id:
            user = self.authenticate_user()
            if not user.student_account.id_student == student_id:
                raise forms.ValidationError('شناسه کاربری دانش آموز مطابقت ندارد')
            self.user = user
        return cd
    
# Sign in form for teachers
class TeacherSigninForm(BaseSigninForm):
    teacher_id = forms.IntegerField(required=True, label='شناسه معلم')

    # Overriding the clean method for checking the teachers id
    def clean(self):
        cd = super().clean()
        teacher_id = cd.get('teacher_id')

        if teacher_id:
            user = self.authenticate_user()
            if not user.teacher_account.id_teacher == teacher_id:
                raise forms.ValidationError('شناسه کاربری مطابقت ندارد')
            self.user = user
        return cd

# Sign in form for parents
class ParentSigninForm(BaseSigninForm):
    student_id = forms.IntegerField(required=True, label='شناسه دانش آموز شما')

    # Overriding the clean method for checking the parents studnt id
    def clean(self):
        cd = super().clean()
        student_id = cd.get('student_id')

        if student_id:
            user = self.authenticate_user()
            if not user.parent_account.children.id_student == student_id:
                raise forms.ValidationError('شناسه کاربری دانش آموز شما مطابقت ندارد')
            self.user = user
        return cd
    
# Ticket form for parents tickets to teachers
class ParentTicketForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, label='موضوع پیام شما')
    description = forms.CharField(max_length=1000, required=True,widget=forms.Textarea, label='متن پیام شما')

# Record score form for teachers to add and change students scores
class RecordScore(forms.Form):
    score = forms.DecimalField(max_digits=4, decimal_places=2, max_value=20, min_value=1, label='نمره')

# Ticket form for teachers to respond to parents tickets
class TicketResponse(forms.Form):
    response = forms.CharField(max_length=1000, label='پاخ پیام')