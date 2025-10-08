"""أمر لتهيئة إعدادات النظام للسوق المصري"""

from django.core.management.base import BaseCommand
from core.models import SystemSettings


class Command(BaseCommand):
    help = 'تهيئة إعدادات النظام للسوق المصري'

    def handle(self, *args, **options):
        settings, created = SystemSettings.objects.get_or_create(
            pk=1,
            defaults={
                'company_name': 'SH Parts - قطع غيار السيارات',
                'company_name_en': 'SH Parts - Auto Parts',
                'currency': 'EGP',
                'default_language': 'ar',
                'timezone': 'Africa/Cairo',
                'tax_enabled': True,
                'tax_rate': 14.00,  # ضريبة القيمة المضافة في مصر
                'city': 'القاهرة',
                'country': 'مصر',
                'low_stock_threshold': 5,
                'allow_negative_stock': False,
                'require_customer_for_sale': True,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ تم إنشاء إعدادات النظام للسوق المصري بنجاح!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ الإعدادات موجودة مسبقاً')
            )
        
        self.stdout.write('\n📋 الإعدادات الحالية:')
        self.stdout.write(f'   العملة: {settings.currency_name} ({settings.currency_symbol})')
        self.stdout.write(f'   الضريبة: {settings.tax_rate}%')
        self.stdout.write(f'   المدينة: {settings.city}')
        self.stdout.write(f'   الدولة: {settings.country}')
