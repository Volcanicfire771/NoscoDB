# models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# 1. Independent models (no foreign keys)
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
    axle_type = models.CharField(max_length=50, default='DRIVE')
    initial_tread_depth = models.DecimalField(max_digits=4, decimal_places=2, default=15.00)
    discarding_tread_depth = models.DecimalField(max_digits=4, decimal_places=2, default=3.00)
    ideal_tire_pressure = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    
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

class TireWearType(models.Model):
    name = models.CharField(max_length=50)
    wear_common_cause = models.CharField(max_length=50)
    recovery_scheme = models.TextField()

    def __str__(self):
        return self.name

# 2. Vehicle (independent, used by many others)
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
    odometer = models.IntegerField(default=0)
    number_of_or_tires = models.IntegerField(default=0)
    number_of_sp_tires = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.license_plate} - {self.make}"

# 3. Tire (depends on TirePattern, TireStatus, Supplier)
class Tire(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    pattern = models.ForeignKey(TirePattern, on_delete=models.PROTECT)
    status = models.ForeignKey(TireStatus, on_delete=models.PROTECT)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True)
    initial_tread_depth = models.DecimalField(max_digits=10, decimal_places=2)
    last_tread_depth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    last_pressure = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # New fields for tracking current location
    current_position = models.ForeignKey(
        'TirePosition', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_tire'
    )
    current_vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_tires'
    )
    is_scrapped = models.BooleanField(default=False)
    
    # Optional: Add this field if you want to track last assignment
    last_assignment = models.ForeignKey(
        'TireAssignment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='last_for_tire'
    )
    
    def __str__(self):
        return self.serial_number
    
    @property
    def can_be_assigned(self):
        """Check if tire is in a state that allows assignment"""
        if self.is_scrapped:
            return False
        
        # Get status name safely
        status_name = self.status.status_name if self.status else ""
        
        # Define invalid statuses for assignment
        invalid_statuses = ['DISCARDED', 'SCRAP', 'SCRAPPED']
        
        # Define valid statuses
        valid_statuses = ['READY', 'MOUNTED', 'ACTIVE', 'IN_STOCK']
        
        # Check both invalid and valid lists
        if status_name in invalid_statuses:
            return False
        
        # If we have valid statuses defined, check against them
        if valid_statuses:
            return status_name in valid_statuses
        
        return True  # Default to True if no specific valid statuses

# 4. TirePosition (depends on Vehicle, Tire)
class TirePosition(models.Model):
    AXLE_TYPES = [
        ('STEERING', 'Steering Axle'),
        ('DRIVE', 'Drive Axle'),
        ('TRAILER', 'Trailer Axle'),
        ('LIFTABLE', 'Liftable Axle'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='tire_positions')
    position_name = models.CharField(max_length=50)
    axle_number = models.IntegerField()
    wheel_number = models.IntegerField()
    axle_type = models.CharField(max_length=20, choices=AXLE_TYPES, default='DRIVE')
    tire_order = models.IntegerField(default=1)
    is_spare = models.BooleanField(default=False)
    
    mounted_tire = models.ForeignKey(
        Tire, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='mounted_positions'
    )

    class Meta:
        unique_together = ['vehicle', 'axle_number', 'wheel_number']
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.position_name}"

# 5. WorkOrder (depends on Employee, Vehicle)
class WorkOrder(models.Model):
    SHIFT_TYPES = [
        ('INSPECTION', 'Tire Inspection'),
        ('ASSIGNMENT', 'Tire Assignment'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('OPENED', 'Opened'),
        ('COMPLETED', 'Completed'),
        ('CLOSED', 'Closed'),
    ]
    
    work_order_number = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    driver_id = models.CharField(max_length=50, blank=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.PROTECT, 
                                  related_name='work_orders')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, 
                              related_name='work_orders')
    current_odometer = models.IntegerField()
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.work_order_number

# 6. MaintenanceRecord (depends on Vehicle, ServiceType, Supplier)
class MaintenanceRecord(models.Model):
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
        return f"{self.vehicle.license_plate} - {self.service_date}"

# 7. TireInspection (depends on Tire, TirePosition, Employee, TireWearType, WorkOrder)
class TireInspection(models.Model):
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE, related_name='inspections')
    position = models.ForeignKey(TirePosition, on_delete=models.CASCADE)
    inspection_odometer = models.IntegerField()
    inspector = models.ForeignKey(Employee, on_delete=models.PROTECT, 
                                related_name='inspections')
    tread_depth = models.DecimalField(max_digits=4, decimal_places=2)
    pressure = models.DecimalField(max_digits=5, decimal_places=2)
    wear_id = models.ForeignKey(TireWearType, on_delete=models.PROTECT)

    # Calculated fields
    consumption_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    remaining_traveling_distance = models.IntegerField(default=0)
    cost_per_mm_tread_depth = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    cost_per_1000_km_travel = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fuel_consumption_increase = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fuel_loss_caused = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    current_tire_value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    balance_traveling_distance = models.IntegerField(default=0)

    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name='tire_inspections',
        null=True, blank=True
    )
    
    inspection_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update tire's latest readings
        self.tire.last_tread_depth = self.tread_depth
        self.tire.last_pressure = self.pressure
        self.tire.save()

    def __str__(self):
        return f"Inspection {self.id} - {self.tire.serial_number}"

# 8. TireAssignment (depends on Tire, TirePosition, WorkOrder, TireInspection)
class TireAssignment(models.Model):
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE, related_name='assignments')
    tire_position_from = models.ForeignKey(TirePosition, on_delete=models.CASCADE, 
                                    related_name='assignments_from', null=True, blank=True)
    tire_position_to = models.ForeignKey(TirePosition, on_delete=models.CASCADE, 
                                  related_name='assignments_to', null=True, blank=True)  # Allow null for discard
    assignment_date = models.DateField()
    removal_date = models.DateField(null=True, blank=True)
    reason_for_removal = models.TextField(blank=True)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, 
                                 related_name='tire_assignments')
    inspection = models.ForeignKey(TireInspection, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='assignments')
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_discard_operation = models.BooleanField(default=False)

    def is_discard(self):
        """Check if this assignment is a discard operation"""
        return self.is_discard_operation or self.tire_position_to is None
    
    def __str__(self):
        if self.is_discard():
            return f"{self.tire.serial_number} - DISCARDED"
        return f"{self.tire.serial_number} - {self.tire_position_to}"
    
    def save(self, *args, **kwargs):
        # Set assignment date to today if not provided
        if not self.assignment_date:
            self.assignment_date = timezone.now().date()
        super().save(*args, **kwargs)

# SIGNALS - Updated to handle discard operations
@receiver(post_save, sender=TireAssignment)
def update_related_models_on_assignment(sender, instance, created, **kwargs):
    """Automatically update related models when assignment is created/updated"""
    if created:
        tire = instance.tire
        
        if instance.is_discard():
            # ====== DISCARD OPERATION ======
            # DON'T update current_position for discard (should be None)
            # DON'T update inspections for discard
            
            # But we should update the tire's last_assignment
            if hasattr(tire, 'last_assignment'):
                tire.last_assignment = instance
                tire.save()
                
        else:
            # ====== NORMAL ASSIGNMENT ======
            to_position = instance.tire_position_to
            
            # Update tire's current position only if to_position exists
            if to_position:
                tire.current_position = to_position
                tire.current_vehicle = to_position.vehicle
                
                # Update last_assignment if field exists
                if hasattr(tire, 'last_assignment'):
                    tire.last_assignment = instance
                
                tire.save()
            
            # Update any inspections on this tire at the old position
            if instance.tire_position_from:
                TireInspection.objects.filter(
                    tire=tire,
                    position=instance.tire_position_from
                ).update(position=to_position, work_order=instance.work_order)