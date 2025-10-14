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
    path('teacher_panel_for_parents/', views.teacher_panel_for_parents, name='teacher_panel_for_parents'),
    path('teacher_profile_for_parents/<int:teacher_id>/', views.teacher_profile_for_prn, name='teacher_profile_for_prn'),
    path('parent_ticket/<int:teacher_id>', views.parent_ticket, name='parent_ticket'),
    path('record_scores/', views.record_scores, name='record_scores'),
    path('ticket_response/', views.ticket_response, name='ticket_response')


]