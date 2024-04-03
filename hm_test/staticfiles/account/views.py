from django.shortcuts import render
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """custom Permission class for Admin"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='admin').exists())