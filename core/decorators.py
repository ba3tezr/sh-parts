"""Decorators للتحكم في الصلاحيات"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """
    Decorator للتحقق من دور المستخدم
    
    مثال:
    @role_required('ADMIN', 'MANAGER')
    def my_view(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.role in roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'ليس لديك صلاحية للوصول لهذه الصفحة')
            return redirect('dashboard')
        
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """Decorator للصفحات التي تتطلب صلاحية Admin فقط"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        messages.error(request, 'هذه الصفحة متاحة لمديري النظام فقط')
        return redirect('dashboard')
    
    return _wrapped_view


def manager_or_admin_required(view_func):
    """Decorator للصفحات التي تتطلب Manager أو Admin"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role in ['ADMIN', 'MANAGER'] or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        messages.error(request, 'ليس لديك صلاحية للوصول لهذه الصفحة')
        return redirect('dashboard')
    
    return _wrapped_view
