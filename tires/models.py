# models.py
from django.db import models

class TireStatus(models.Model):
    status_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.status_name

class TirePattern(models.Model):
    pattern_code = models.CharField(max_length=50, unique=True)
    brand_name = models.CharField(max_length=100)
    country_of_origin = models.CharField(max_length=50)
    load_index = models.CharField(max_length=10)
    speed_symbol = models.CharField(max_length=5)
    road_type = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.brand_name} - {self.pattern_code}"

class ServiceType(models.Model):
    service_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.service_name

class Employee(models.Model):
    employment_code = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    evaluation = models.TextField(blank=True)
    
    def __str__(self):
        return self.supplier_name


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('TRUCK', 'Truck'),
        ('TRAILER', 'Trailer'),
        ('BUS', 'Bus'),
        ('VAN', 'Van'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('MAINTENANCE', 'Under Maintenance'),
    ]
    
    license_plate = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50)
    year = models.IntegerField()
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    tire_configuration = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.license_plate} - {self.make}"

class TirePosition(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='tire_positions')
    position_name = models.CharField(max_length=50)
    axle_number = models.IntegerField()
    wheel_number = models.IntegerField()
    is_spare = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['vehicle', 'axle_number', 'wheel_number']
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.position_name}"
    
class Tire(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    pattern = models.ForeignKey(TirePattern, on_delete=models.PROTECT)
    status = models.ForeignKey(TireStatus, on_delete=models.PROTECT)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True)
    initial_tread_depth = models.DecimalField(max_digits=4, decimal_places=2)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.serial_number

class TireAssignment(models.Model):
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE, related_name='assignments')
    from_position = models.ForeignKey(TirePosition, on_delete=models.CASCADE, 
                                    related_name='assignments_from', null=True, blank=True)
    to_position = models.ForeignKey(TirePosition, on_delete=models.CASCADE, 
                                  related_name='assignments_to')
    assignment_date = models.DateField()
    removal_date = models.DateField(null=True, blank=True)
    start_odometer = models.IntegerField()
    end_odometer = models.IntegerField(null=True, blank=True)
    removal_mileage = models.IntegerField(null=True, blank=True)
    reason_for_removal = models.TextField(blank=True)
    work_order = models.ForeignKey('WorkOrder', on_delete=models.CASCADE, 
                                 related_name='tire_assignments')
    inspector = models.ForeignKey(Employee, on_delete=models.PROTECT, 
                                related_name='tire_assignments')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.tire.serial_number} - {self.to_position}"

class WorkOrder(models.Model):
    SHIFT_TYPES = [
        ('INSTALLATION', 'Tire Installation'),
        ('REMOVAL', 'Tire Removal'),
        ('ROTATION', 'Tire Rotation'),
        ('REPAIR', 'Tire Repair'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    work_order_number = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.PROTECT, 
                                  related_name='work_orders')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, 
                              related_name='work_orders')
    current_mileage = models.IntegerField()
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.work_order_number
    
class TireInspection(models.Model):
    RECOMMENDED_ACTIONS = [
        ('OK', 'OK - No Action Needed'),
        ('ROTATE', 'Rotate Tire'),
        ('REPAIR', 'Repair Needed'),
        ('REPLACE', 'Replace Tire'),
        ('PRESSURE_ADJUST', 'Adjust Pressure'),
    ]
    
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE, related_name='inspections')
    position = models.ForeignKey(TirePosition, on_delete=models.CASCADE)
    inspection_odometer = models.IntegerField()
    inspector = models.ForeignKey(Employee, on_delete=models.PROTECT, 
                                related_name='inspections')
    driver_id = models.CharField(max_length=50, blank=True)
    tread_depth = models.DecimalField(max_digits=4, decimal_places=2)
    pressure = models.DecimalField(max_digits=5, decimal_places=2)
    tire_consumption = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recommended_action = models.CharField(max_length=20, choices=RECOMMENDED_ACTIONS)
    inspection_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tire.serial_number} - {self.inspection_date}"

class MaintenanceRecord(models.Model):
    maintenance_id = models.CharField(max_length=50, unique=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, 
                              related_name='maintenance_records')
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    service_date = models.DateField()
    service_mileage = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_provider = models.ForeignKey(Supplier, on_delete=models.PROTECT, 
                                       related_name='maintenance_services')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.maintenance_id