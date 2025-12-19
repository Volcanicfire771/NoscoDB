from django.urls import path
from .views.employee import *
from .views.maintainance_record import *
from .views.menu import *
from .views.service_type import *
from .views.supplier import *
from .views.tire_assignment import *
from .views.tire_inspection import *
from .views.tire_pattern import *
from .views.tire_position import *
from .views.tire_status import *
from .views.tires import *
from .views.vehicles import *
from .views.work_order import *
from .views.tire_wear import *



urlpatterns = [
    # Menu
    path('',  menu_page, name='menu_page'),

    # Vehicle URLs
    path('vehicles/', vehicle_list, name='vehicle_list'),
    path('vehicles/create/', vehicle_create, name='vehicle_create'),
    path('vehicles/update/<int:id>/', vehicle_update, name='vehicle_update'),
    path('vehicles/delete/<int:id>/', vehicle_delete, name='vehicle_delete'),
    
    # Tire Status URLs
    path('tire-status/',  tire_status_list, name='tire_status_list'),
    path('tire-status/create/', tire_status_create, name='tire_status_create'),
    path('tire-status/update/<int:id>/', tire_status_update, name='tire_status_update'),
    path('tire-status/delete/<int:id>/', tire_status_delete, name='tire_status_delete'),
    
    # Service Type URLs
    path('service-types/', service_type_list, name='service_type_list'),
    path('service-types/create/', service_type_create, name='service_type_create'),
    path('service-types/update/<int:id>/', service_type_update, name='service_type_update'),
    path('service-types/delete/<int:id>/', service_type_delete, name='service_type_delete'),
    
    # Supplier URLs
    path('suppliers/', supplier_list, name='supplier_list'),
    path('suppliers/create/', supplier_create, name='supplier_create'),
    path('suppliers/update/<int:id>/', supplier_update, name='supplier_update'),
    path('suppliers/delete/<int:id>/', supplier_delete, name='supplier_delete'),
    
    # Employee URLs
    path('employees/', employee_list, name='employee_list'),
    path('employees/create/', employee_create, name='employee_create'),
    path('employees/update/<int:id>/', employee_update, name='employee_update'),
    path('employees/delete/<int:id>/', employee_delete, name='employee_delete'),

    # Work Order URLs
    path('work-orders/', work_order_list, name='work_order_list'),
    path('work-orders/create/', work_order_create, name='work_order_create'),
    path('work-orders/update/<int:id>/', work_order_update, name='work_order_update'),
    path('work-orders/delete/<int:id>/', work_order_delete, name='work_order_delete'),

    # Tire Position URLs
    path('tire-position/', tire_position_list, name='tire_position_list'),
    path('tire-position/create/', tire_position_create, name='tire_position_create'),
    path('tire-position/update/<int:id>/', tire_position_update, name='tire_position_update'),
    path('tire-position/delete/<int:id>/', tire_position_delete, name='tire_position_delete'),

    # Maintenance Records URLs
    path('maintainance-records/', maintenance_records_list, name='maintenance_records_list'),
    path('maintainance-records/create/', maintenance_records_create, name='maintenance_records_create'),
    path('maintainance-records/update/<int:id>/', maintenance_records_update, name='maintenance_records_update'),
    path('maintainance-records/delete/<int:id>/', maintenance_records_delete, name='maintenance_records_delete'),

    # Tire Inspections URLs
    path('tire-inspections/', tire_inspections_list, name='tire_inspections_list'),
    path('tire-inspections/create/', tire_inspections_create, name='tire_inspections_create'),
    path('tire-inspections/update/<int:id>/', tire_inspections_update, name='tire_inspections_update'),
    path('tire-inspections/delete/<int:id>/', tire_inspections_delete, name='tire_inspections_delete'),
    path("tire-inspections/bulk-update/", bulk_tire_update, name="bulk_tire_update"),

    # Tires URLS
    path('tires/', tires_list, name='tires_list'),
    path('tires/create/', tires_create, name='tires_create'),
    path('tires/update/<int:id>/', tires_update, name='tires_update'),
    path('tires/delete/<int:id>/', tires_delete, name='tires_delete'),

    # Tires Pattern URLS
    path('tire-patterns/', tire_patterns_list, name='tire_patterns_list'),
    path('tire-patterns/create/', tire_patterns_create, name='tire_patterns_create'),
    path('tire-patterns/update/<int:id>/', tire_patterns_update, name='tire_patterns_update'),
    path('tire-patterns/delete/<int:id>/', tire_patterns_delete, name='tire_patterns_delete'),

    # Tire Assignment URLS
     path('tire-assignments/', tire_assignment_list, name='tire_assignment_list'),
    path('tire-assignments/create/', tire_assignment_create, name='tire_assignment_create'),
    path('tire-assignments/<int:id>/update/', tire_assignment_update, name='tire_assignment_update'),
    path('tire-assignments/<int:id>/delete/', tire_assignment_delete, name='tire_assignment_delete'),
    # Tire Wear URLS
    path('tire-wear-type/', tire_wear_type_list, name='tire_wear_type_list'),
    path('tire-wear-type/create/', tire_wear_type_create, name='tire_wear_type_create'),
    path('tire-wear-type/update/<int:id>/', tire_wear_type_update, name='tire_wear_type_update'),
    path('tire-wear-type/delete/<int:id>/', tire_wear_type_delete, name='tire_wear_type_delete'),

]