from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SavedReport, ReportExecution


@admin.register(SavedReport)
class SavedReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'is_public', 'is_scheduled', 'created_by', 'created_at', 'last_run')
    list_filter = ('report_type', 'is_public', 'is_scheduled', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'last_run')
    
    fieldsets = (
        (_('Report Information'), {
            'fields': ('name', 'report_type', 'description')
        }),
        (_('Configuration'), {
            'fields': ('filters', 'columns')
        }),
        (_('Settings'), {
            'fields': ('is_public', 'is_scheduled', 'schedule_frequency')
        }),
        (_('Metadata'), {
            'fields': ('created_by', 'created_at', 'updated_at', 'last_run'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReportExecution)
class ReportExecutionAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'status', 'file_format', 'executed_by', 'started_at', 'completed_at')
    list_filter = ('report_type', 'status', 'file_format', 'started_at')
    search_fields = ('report_type', 'executed_by__email')
    date_hierarchy = 'started_at'
    readonly_fields = ('started_at', 'completed_at')
    
    fieldsets = (
        (_('Execution Details'), {
            'fields': ('saved_report', 'report_type', 'parameters', 'status', 'error_message')
        }),
        (_('Output'), {
            'fields': ('file_path', 'file_format')
        }),
        (_('Metadata'), {
            'fields': ('executed_by', 'started_at', 'completed_at')
        }),
    )
