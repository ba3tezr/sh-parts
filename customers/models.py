from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('INDIVIDUAL', _('Individual')),
        ('BUSINESS', _('Business')),
    ]

    customer_code = models.CharField(_('customer code'), max_length=20, unique=True, editable=False)
    customer_type = models.CharField(_('customer type'), max_length=20, 
                                    choices=CUSTOMER_TYPE_CHOICES, default='INDIVIDUAL')
    
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    business_name = models.CharField(_('business name'), max_length=200, blank=True)
    
    email = models.EmailField(_('email'), blank=True)
    phone = models.CharField(_('phone'), max_length=20)
    phone_secondary = models.CharField(_('secondary phone'), max_length=20, blank=True)
    
    address_line1 = models.CharField(_('address line 1'), max_length=200, blank=True)
    address_line2 = models.CharField(_('address line 2'), max_length=200, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state/province'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    country = models.CharField(_('country'), max_length=100, default='Saudi Arabia')
    
    tax_id = models.CharField(_('tax ID'), max_length=50, blank=True)
    credit_limit = models.DecimalField(_('credit limit'), max_digits=10, decimal_places=2, 
                                      default=0.00)
    
    notes = models.TextField(_('notes'), blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                  related_name='created_customers', verbose_name=_('created by'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer_code']),
            models.Index(fields=['phone']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        if self.customer_type == 'BUSINESS' and self.business_name:
            return f"{self.customer_code} - {self.business_name}"
        return f"{self.customer_code} - {self.get_full_name()}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.customer_code:
            self.customer_code = self.generate_customer_code()
        super().save(*args, **kwargs)

    def generate_customer_code(self):
        import random
        import string
        from django.utils import timezone
        
        timestamp = timezone.now().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.digits, k=4))
        return f"CUST-{timestamp}-{random_str}"

    @property
    def total_purchases(self):
        from sales.models import Sale
        return Sale.objects.filter(customer=self, status='COMPLETED').aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0

    @property
    def outstanding_balance(self):
        from sales.models import Sale
        sales = Sale.objects.filter(customer=self, payment_status__in=['PARTIAL', 'UNPAID'])
        total = sum(sale.total_amount - sale.paid_amount for sale in sales)
        return total


class CustomerCredit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, 
                                related_name='credits', verbose_name=_('customer'))
    credit_amount = models.DecimalField(_('credit amount'), max_digits=10, decimal_places=2)
    reason = models.TextField(_('reason'))
    reference = models.CharField(_('reference'), max_length=100, blank=True)
    
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                 related_name='issued_credits', verbose_name=_('issued by'))
    issued_at = models.DateTimeField(_('issued at'), auto_now_add=True)
    
    is_used = models.BooleanField(_('used'), default=False)
    used_at = models.DateTimeField(_('used at'), null=True, blank=True)

    class Meta:
        verbose_name = _('customer credit')
        verbose_name_plural = _('customer credits')
        ordering = ['-issued_at']

    def __str__(self):
        return f"Credit {self.credit_amount} for {self.customer.customer_code}"


class CustomerNote(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, 
                                related_name='customer_notes', verbose_name=_('customer'))
    note = models.TextField(_('note'))
    is_important = models.BooleanField(_('important'), default=False)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                  related_name='customer_notes', verbose_name=_('created by'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('customer note')
        verbose_name_plural = _('customer notes')
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.customer.customer_code}"
