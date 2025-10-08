"""Context Processors لتوفير الإعدادات في جميع القوالب"""

from .models import SystemSettings


def system_settings(request):
    """إضافة إعدادات النظام لكل القوالب"""
    settings = SystemSettings.get_settings()
    return {
        'system_settings': settings,
        'currency': settings.currency,
        'currency_symbol': settings.currency_symbol,
    }
