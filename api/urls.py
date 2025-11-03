from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from . import views

router1 = DefaultRouter()
router1.register(r"terms", views.StudentTermAPIView)
router2 = DefaultRouter()
router2.register(r"students", views.StudentAccountAPIView)

urlpatterns = [
    path('users/', views.UserApiView.as_view(), name='users_api_view'),
    path('user/register/', views.UserAPIRegistrationView.as_view(), name='user_api_registration'),
    path('parent/', views.ParentListApiView.as_view(), name='parent-list-api'),
    # path('students/', views.StudentListApiView.as_view(), name='students-list-api'),
    # path('students/<pk>/', views.StudentDetailApiView.as_view(), name='students-detail-list-api'),
    path('', include(router1.urls)),
    path('', include(router2.urls)),
]