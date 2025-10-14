"""Middleware لإدارة الصلاحيات وتسجيل النشاطات"""

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import translation
from django.conf import settings


class RoleBasedAccessMiddleware:
    """
    Middleware للتحكم في الوصول بناءً على أدوار المستخدمين
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # تحديد الصفحات المحمية وأدوار الوصول المطلوبة
        self.protected_paths = {
            '/admin/': ['ADMIN'],
            '/reports/': ['ADMIN', 'MANAGER'],
        }
    
    def __call__(self, request):
        # السماح بالوصول لصفحات تسجيل الدخول والخروج
        if request.path in [reverse('login'), reverse('logout')]:
            return self.get_response(request)
        
        # السماح بالوصول للملفات الثابتة و API
        if request.path.startswith('/static/') or request.path.startswith('/media/') or request.path.startswith('/api/'):
            return self.get_response(request)
        
        # التحقق من الصفحات المحمية
        if request.user.is_authenticated:
            for path, required_roles in self.protected_paths.items():
                if request.path.startswith(path):
                    # السماح للـ superuser دائماً
                    if request.user.is_superuser:
                        break
                    
                    # التحقق من الدور
                    if hasattr(request.user, 'role') and request.user.role not in required_roles:
                        messages.error(request, 'ليس لديك صلاحية للوصول لهذه الصفحة')
                        return redirect('dashboard')
        
        response = self.get_response(request)
        return response


class ForceDefaultLanguageMiddleware:
    """
    Middleware لإجبار اللغة الافتراضية (العربية) إذا لم يتم تحديد لغة في الجلسة
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # التحقق من وجود لغة محددة في الجلسة أو الكوكيز
        language_session_key = '_language'  # Django's default session key for language

        if not request.session.get(language_session_key):
            # إذا لم توجد لغة محددة، استخدم اللغة الافتراضية من settings
            language = settings.LANGUAGE_CODE
            translation.activate(language)
            request.LANGUAGE_CODE = language
            request.session[language_session_key] = language

        response = self.get_response(request)
        return response


class UserActivityLogMiddleware:
    """
    Middleware لتسجيل نشاطات المستخدمين (اختياري)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # يمكن إضافة تسجيل النشاطات هنا
        # مثل: تسجيل الصفحات المزورة، العمليات المنفذة، إلخ

        return response
