from rest_framework import permissions

class MyCustomPermission(permissions.BasePermission):
    
    # the response should be a True or False
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and \
            user.is_superuser and \
            user.user_type == 'mng'

class IsAllowedToSee(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True 
    