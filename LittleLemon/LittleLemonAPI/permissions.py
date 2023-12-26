from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is in the "Manager" group
        return request.user.groups.filter(name='Manager').exists()
    


