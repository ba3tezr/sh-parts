from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class SavedReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('INVENTORY_VALUATION', _('Inventory Valuation')),
        ('SALES_SUMMARY', _('Sales Summary')),
        ('SALES_BY_PART', _('Sales by Part')),
        ('SALES_BY_CUSTOMER', _('Sales by Customer')),
        ('CUSTOMER_DEBT', _('Customer Debt')),
        ('STOCK_MOVEMENT', _('Stock Movement')),
        ('LOW_STOCK', _('Low Stock Alert')),
        ('PROFIT_MARGIN', _('Profit Margin Analysis')),
        ('VEHICLE_INTAKE', _('Vehicle Intake Report')),
        ('CUSTOM', _('Custom Report')),
    ]

    name = models.CharField(_('report name'), max_length=200)
    report_type = models.CharField(_('report type'), max_length=50, choices=REPORT_TYPE_CHOICES)
    description = models.TextField(_('description'), blank=True)
    
    filters = models.JSONField(_('filters'), default=dict, blank=True)
    columns = models.JSONField(_('columns'), default=list, blank=True)
    
    is_public = models.BooleanField(_('public'), default=False)
    is_scheduled = models.BooleanField(_('scheduled'), default=False)
    schedule_frequency = models.CharField(_('schedule frequency'), max_length=20, blank=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='saved_reports', verbose_name=_('created by'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    last_run = models.DateTimeField(_('last run'), null=True, blank=True)

    class Meta:
        verbose_name = _('saved report')
        verbose_name_plural = _('saved reports')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ReportExecution(models.Model):
    saved_report = models.ForeignKey(SavedReport, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='executions', verbose_name=_('saved report'))
    
    report_type = models.CharField(_('report type'), max_length=50)
    parameters = models.JSONField(_('parameters'), default=dict)
    
    file_path = models.CharField(_('file path'), max_length=500, blank=True)
    file_format = models.CharField(_('file format'), max_length=10)
    
    status = models.CharField(_('status'), max_length=20, default='PENDING')
    error_message = models.TextField(_('error message'), blank=True)
    
    executed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='report_executions', verbose_name=_('executed by'))
    started_at = models.DateTimeField(_('started at'), auto_now_add=True)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)

    class Meta:
        verbose_name = _('report execution')
        verbose_name_plural = _('report executions')
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.report_type} - {self.started_at}"
