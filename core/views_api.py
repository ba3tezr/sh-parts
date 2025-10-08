"""API للحصول على إعدادات النظام"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import SystemSettings


@api_view(['GET'])
@permission_classes([AllowAny])  # السماح للجميع بالوصول للإعدادات
def get_system_settings(request):
    """الحصول على إعدادات النظام للواجهة الأمامية"""
    settings = SystemSettings.get_settings()
    
    return Response({
        'currency': settings.currency,
        'currency_symbol': settings.currency_symbol,
        'currency_name': settings.currency_name,
        'tax_enabled': settings.tax_enabled,
        'tax_rate': float(settings.tax_rate),
        'default_language': settings.default_language,
        'timezone': settings.timezone,
        'company_name': settings.company_name,
        'company_name_en': settings.company_name_en,
    })
