from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'EMPLOYEE'

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'CUSTOMER'