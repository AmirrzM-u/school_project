from django import forms
from .models import *
from django.contrib.auth import authenticate

class StudentSigninForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='نام کاربری یا شماره تلفن همراه')
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput, label='رمز عبور')
    student_id = forms.IntegerField(required=True, label='شناسه دانش آموز')


    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')
        student_id = cd.get('student_id')

        if (username and password and student_id):
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('نام کاربری یا رمز عبور اشتباه است')
            if user.student_account.id_student != student_id:
                raise forms.ValidationError('شناسه کاربری دانش آموز مطابقت ندارد')
            self.user = user
        return cd
    
class TeacherSigninForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='نام کاربری یا شماره تلفن همراه')
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput, label='رمز عبور')
    teacher_id = forms.IntegerField(required=True, label='شناسه معلم')


    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')
        teacher_id = cd.get('student_id')

        if (username and password and teacher_id):
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('نام کاربری یا رمز عبور اشتباه است')
            if user.teacher_account.id_teacher != teacher_id:
                raise forms.ValidationError('شناسه کاربری مطابقت ندارد')
            self.user = user
        return cd
    
class ParentSigninForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='نام کاربری یا شماره تلفن همراه')
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput, label='رمز عبور')
    student_id = forms.IntegerField(required=True, label='شناسه دانش آموز شما')


    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')
        student_id = cd.get('student_id')

        if (username and password and student_id):
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('نام کاربری یا رمز عبور اشتباه است')
            if user.parent_account.children.id_student != student_id:
                raise forms.ValidationError('شناسه کاربری دانش آموز شما مطابقت ندارد')
            self.user = user
        return cd