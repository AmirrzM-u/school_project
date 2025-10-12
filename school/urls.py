from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/<int:news_id>', views.news_detail, name='news_details'),
    path('student_sign-in/<str:user_type>', views.user_signin, name='user_student_signin'),
    path('teacher_sign-in/<str:user_type>', views.user_signin, name='user_teacher_signin'),
    path('parent_sign-in/<str:user_type>', views.user_signin, name='user_parent_signin'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('student_scores/', views.student_scores, name='student_scores'),
    path('student_schedule/', views.student_schedule, name='student_schedule'),
    path('teacher_panel_for_parents/', views.teacher_panel_for_parents, name='teacher_panel_for_parents')
]