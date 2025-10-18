from django.urls import path
from . import views

urlpatterns = [
    # Vehicle URLs
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/update/<int:id>/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/delete/<int:id>/', views.vehicle_delete, name='vehicle_delete'),
    
    # Tire Status URLs
    path('tire-status/', views.tire_status_list, name='tire_status_list'),
    path('tire-status/create/', views.tire_status_create, name='tire_status_create'),
    path('tire-status/update/<int:id>/', views.tire_status_update, name='tire_status_update'),
    path('tire-status/delete/<int:id>/', views.tire_status_delete, name='tire_status_delete'),
    
    # Service Type URLs
    path('service-types/', views.service_type_list, name='service_type_list'),
    path('service-types/create/', views.service_type_create, name='service_type_create'),
    path('service-types/update/<int:id>/', views.service_type_update, name='service_type_update'),
    path('service-types/delete/<int:id>/', views.service_type_delete, name='service_type_delete'),
    
    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/update/<int:id>/', views.supplier_update, name='supplier_update'),
    path('suppliers/delete/<int:id>/', views.supplier_delete, name='supplier_delete'),
    
    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/update/<int:id>/', views.employee_update, name='employee_update'),
    path('employees/delete/<int:id>/', views.employee_delete, name='employee_delete'),

    # Work Order URLs
    path('work-orders/', views.work_order_list, name='work_order_list'),
    path('work-orders/create/', views.work_order_create, name='work_order_create'),
    path('work-orders/update/<int:id>/', views.work_order_update, name='work_order_update'),
    path('work-orders/delete/<int:id>/', views.work_order_delete, name='work_order_delete'),

    # Tire Position URLs
    path('tire-position/', views.tire_position_list, name='tire_position_list'),
    path('tire-position/create/', views.tire_position_create, name='tire_position_create'),
    path('tire-position/update/<int:id>/', views.tire_position_update, name='tire_position_update'),
    path('tire-position/delete/<int:id>/', views.tire_position_delete, name='tire_position_delete'),

    # Maintenance Records URLs
    path('maintainance-records/', views.maintenance_records_list, name='maintenance_records_list'),
    path('maintainance-records/create/', views.maintenance_records_create, name='maintenance_records_create'),
    path('maintainance-records/update/<int:id>/', views.maintenance_records_update, name='maintenance_records_update'),
    path('maintainance-records/delete/<int:id>/', views.maintenance_records_delete, name='maintenance_records_delete'),

    # Tire Inspections URLs
    path('tire-inspections/', views.tire_inspections_list, name='tire_inspections_list'),
    path('tire-inspections/create/', views.tire_inspections_create, name='tire_inspections_create'),
    path('tire-inspections/update/<int:id>/', views.tire_inspections_update, name='tire_inspections_update'),
    path('tire-inspections/delete/<int:id>/', views.tire_inspections_delete, name='tire_inspections_delete'),

    # Tires URLS
    path('tires/', views.tires_list, name='tires_list'),
    path('tires/create/', views.tires_create, name='tires_create'),
    path('tires/update/<int:id>/', views.tires_update, name='tires_update'),
    path('tires/delete/<int:id>/', views.tires_delete, name='tires_delete'),

    # Tires Pattern URLS
    path('tire-patterns/', views.tire_patterns_list, name='tire_patterns_list'),
    path('tire-patterns/create/', views.tire_patterns_create, name='tire_patterns_create'),
    path('tire-patterns/update/<int:id>/', views.tire_patterns_update, name='tire_patterns_update'),
    path('tire-patterns/delete/<int:id>/', views.tire_patterns_delete, name='tire_patterns_delete'),

    # Tire Assignment URLS
    path('tire-assignment/', views.tire_assignment_list, name='tire_assignment_list'),
    path('tire-assignment/create/', views.tire_assignment_create, name='tire_assignment_create'),
    path('tire-assignment/update/<int:id>/', views.tire_assignment_update, name='tire_assignment_update'),
    path('tire-assignment/delete/<int:id>/', views.tire_assignment_delete, name='tire_assignment_delete'),
]