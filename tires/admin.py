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