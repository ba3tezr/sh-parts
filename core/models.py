from django.db import models
from django.core.cache import cache


class SystemSettings(models.Model):
    """إعدادات النظام - System Settings"""
    
    CURRENCY_CHOICES = [
        ('EGP', 'الجنيه المصري - Egyptian Pound (EGP)'),
        ('SAR', 'الريال السعودي - Saudi Riyal (SAR)'),
        ('AED', 'الدرهم الإماراتي - UAE Dirham (AED)'),
        ('USD', 'الدولار الأمريكي - US Dollar (USD)'),
        ('EUR', 'اليورو - Euro (EUR)'),
    ]
    
    CURRENCY_SYMBOLS = {
        'EGP': 'ج.م',
        'SAR': 'ر.س',
        'AED': 'د.إ',
        'USD': '$',
        'EUR': '€',
    }
    
    LANGUAGE_CHOICES = [
        ('ar', 'العربية'),
        ('en', 'English'),
    ]
    
    TIMEZONE_CHOICES = [
        ('Africa/Cairo', 'القاهرة (مصر)'),
        ('Asia/Riyadh', 'الرياض (السعودية)'),
        ('Asia/Dubai', 'دبي (الإمارات)'),
        ('UTC', 'UTC'),
    ]
    
    # معلومات الشركة - Company Information
    company_name = models.CharField(
        'اسم الشركة',
        max_length=255,
        default='SH Parts'
    )
    company_name_en = models.CharField(
        'اسم الشركة بالإنجليزية',
        max_length=255,
        default='SH Parts'
    )
    
    # إعدادات العملة - Currency Settings
    currency = models.CharField(
        'العملة',
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='EGP'
    )
    
    # إعدادات اللغة والمنطقة - Language and Region
    default_language = models.CharField(
        'اللغة الافتراضية',
        max_length=5,
        choices=LANGUAGE_CHOICES,
        default='ar'
    )
    timezone = models.CharField(
        'المنطقة الزمنية',
        max_length=50,
        choices=TIMEZONE_CHOICES,
        default='Africa/Cairo'
    )
    
    # إعدادات الضرائب - Tax Settings
    tax_enabled = models.BooleanField(
        'تفعيل الضرائب',
        default=True
    )
    tax_rate = models.DecimalField(
        'نسبة الضريبة (%)',
        max_digits=5,
        decimal_places=2,
        default=14.00,  # ضريبة القيمة المضافة في مصر
        help_text='نسبة الضريبة المضافة (مصر: 14%، السعودية: 15%)'
    )
    tax_number = models.CharField(
        'الرقم الضريبي',
        max_length=50,
        blank=True,
        null=True
    )
    
    # معلومات الاتصال - Contact Information
    phone = models.CharField(
        'الهاتف',
        max_length=20,
        blank=True,
        null=True
    )
    email = models.EmailField(
        'البريد الإلكتروني',
        blank=True,
        null=True
    )
    address = models.TextField(
        'العنوان',
        blank=True,
        null=True
    )
    city = models.CharField(
        'المدينة',
        max_length=100,
        default='القاهرة'
    )
    country = models.CharField(
        'الدولة',
        max_length=100,
        default='مصر'
    )
    
    # إعدادات المخزون - Inventory Settings
    low_stock_threshold = models.IntegerField(
        'حد تنبيه المخزون المنخفض',
        default=5,
        help_text='التنبيه عندما تقل الكمية عن هذا الرقم'
    )
    
    # إعدادات النظام - System Settings
    allow_negative_stock = models.BooleanField(
        'السماح بالمخزون السالب',
        default=False
    )
    require_customer_for_sale = models.BooleanField(
        'إلزامية العميل في المبيعات',
        default=True
    )
    
    # التواريخ - Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='settings_updates'
    )
    
    class Meta:
        verbose_name = 'إعدادات النظام'
        verbose_name_plural = 'إعدادات النظام'
    
    def __str__(self):
        return f'إعدادات {self.company_name}'
    
    def save(self, *args, **kwargs):
        # مسح الكاش عند التحديث
        cache.delete('system_settings')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """الحصول على الإعدادات (مع الكاش)"""
        settings = cache.get('system_settings')
        if settings is None:
            settings, created = cls.objects.get_or_create(pk=1)
            cache.set('system_settings', settings, 3600)  # كاش لمدة ساعة
        return settings
    
    @property
    def currency_symbol(self):
        """رمز العملة"""
        return self.CURRENCY_SYMBOLS.get(self.currency, self.currency)
    
    @property
    def currency_name(self):
        """اسم العملة"""
        return dict(self.CURRENCY_CHOICES).get(self.currency, self.currency)
