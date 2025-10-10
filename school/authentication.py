from django.contrib.auth.models import User
from .models import StudentAccount, TeacherAccount, ParentAccount

class PhonenumberAuthBackend:
    def authenticate(self, request, username=None, password=None):
        pass