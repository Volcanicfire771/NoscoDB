# admin.py
from django.contrib import admin
from .models import *

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'make', 'year', 'vehicle_type', 'status']
    list_filter = ['vehicle_type', 'status', 'year']
    search_fields = ['license_plate', 'make']

@admin.register(Tire)
class TireAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'pattern', 'status', 'purchase_date']
    list_filter = ['status', 'pattern__brand_name']
    search_fields = ['serial_number']

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['work_order_number', 'vehicle', 'shift_type', 'status', 'date_created']
    list_filter = ['shift_type', 'status', 'date_created']
    search_fields = ['work_order_number', 'vehicle__license_plate']

@admin.register(ImportStaging)
class ImportStagingAdmin(admin.ModelAdmin):
    list_display = ('ROW_NUMBER', 'SESSION_ID', 'STATUS', 'CREATED_AT')
    list_filter = ('STATUS', 'MODEL_TYPE', 'CREATED_AT')
    search_fields = ('SESSION_ID', 'ROW_NUMBER')
    readonly_fields = ('CREATED_AT', 'UPDATED_AT')
    actions = ['mark_approved', 'mark_rejected']
    
    def mark_approved(self, request, queryset):
        queryset.update(STATUS='approved')
    
    def mark_rejected(self, request, queryset):
        queryset.update(STATUS='rejected')

@admin.register(ImportTemplate)
class ImportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'import_type', 'created_by', 'usage_count', 'created_at')
    list_filter = ('import_type', 'is_public', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ImportLog)
class ImportLogAdmin(admin.ModelAdmin):
    list_display = ('import_type', 'imported_by', 'imported_rows', 'failed_rows', 'created_at')
    list_filter = ('import_type', 'created_at', 'imported_by')
    search_fields = ('session_id', 'file_name')
    readonly_fields = ('session_id', 'created_at', 'stats')

# Register other models similarly...
admin.site.register(TireStatus)
admin.site.register(TirePattern)
admin.site.register(ServiceType)
admin.site.register(Employee)
admin.site.register(Supplier)
admin.site.register(TirePosition)
admin.site.register(TireAssignment)
admin.site.register(TireInspection)
admin.site.register(MaintenanceRecord)
admin.site.register(TireWearType)