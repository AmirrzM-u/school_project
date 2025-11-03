from django.shortcuts import render
from school.models import StudentAccount, User, StudentTerm
from rest_framework import generics
from .serializers import *
from rest_framework import views
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from rest_framework .response import Response
from rest_framework import viewsets
from .permission import MyCustomPermission, IsAllowedToSee
from rest_framework.decorators import action


class UserApiView(views.APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [MyCustomPermission]
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerialier(users, many=True)
        return Response(serializer.data)
    
class UserAPIRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class ParentListApiView(generics.ListAPIView):
    queryset = ParentAccount.objects.all()
    serializer_class = ParentAccountSerializer

# class StudentListApiView(generics.ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = StudentAccount.objects.all()
#     serializer_class = StudentAccountSerializer

# class StudentDetailApiView(generics.RetrieveAPIView):
#     permission_classes = [IsAllowedToSee]
#     queryset = StudentAccount.objects.all()
#     serializer_class = StudentAccountSerializer

class StudentAccountAPIView(viewsets.ModelViewSet):
    queryset = StudentAccount.objects.all()
    serializer_class = StudentAccountSerializer
    permission_classes = [AllowAny]
    # action is a custom CRUD that you determine
    @action(detail=False, methods=['get'])
    def top_10_student(self, request):
        top_stds = self.queryset.filter(grade_level='11').order_by('-avg_1')[:5]
        serializer = self.get_serializer(top_stds, many=True)
        return Response(serializer.data)

class StudentTermAPIView(viewsets.ModelViewSet):
    queryset = StudentTerm.objects.all()
    serializer_class = StudentTermSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]



