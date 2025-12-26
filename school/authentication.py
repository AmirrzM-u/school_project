from .models import User

# Custom Authentication Backend  
# Allows users to login using their phone number instead of username
class PhonenumberAuthBackend:

    # usrename is treated as phone number here
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(phone_number=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        