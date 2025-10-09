from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/<int:news_id>', views.news_detail, name='news_details'),
    path('sign-in/', views.user_signin, name='user_signin')
]