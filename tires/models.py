# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder

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
    axle_type = models.CharField(max_length=50, default='DRIVE')  # ADDED DEFAULT
    initial_tread_depth = models.DecimalField(max_digits=4, decimal_places=2, default=15.00)  # ADDED DEFAULT
    discarding_tread_depth = models.DecimalField(max_digits=4, decimal_places=2, default=3.00)  # ADDED DEFAULT
    ideal_tire_pressure = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)  # ADDED DEFAULT
    
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
    odometer = models.IntegerField(default=0)
    number_of_or_tires = models.IntegerField(default=0)
    number_of_sp_tires = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.license_plate} - {self.make}"

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
    axle_type = models.CharField(max_length=20, choices=AXLE_TYPES, default='DRIVE')  # ADDED DEFAULT
    tire_order = models.IntegerField(default=1)
    is_spare = models.BooleanField(default=False)
    
    mounted_tire = models.ForeignKey(
        'Tire', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='mounted_positions'
    )

    class Meta:
        unique_together = ['vehicle', 'axle_number', 'wheel_number']
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.position_name}"

class Tire(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    pattern = models.ForeignKey(TirePattern, on_delete=models.PROTECT)
    size = models.CharField(max_length=50)
    status = models.ForeignKey(TireStatus, on_delete=models.PROTECT)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True)
    initial_tread_depth = models.DecimalField(max_digits=10, decimal_places=2)
    last_tread_depth = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    # last_pressure = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    retread_count = models.IntegerField(null=True, blank=True)
    maximum_retreads = models.IntegerField(null=True, blank=True)
    current_position = models.ForeignKey(TirePosition, on_delete=models.SET_NULL, 
                                     null=True, blank=True, related_name='current_tires')
    tire_mileage = models.IntegerField(null=True, blank=True)
    # last_assignment = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    

    def __str__(self):
        return self.serial_number

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
    current_odometer = models.IntegerField()  # Renamed from current_mileage
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.work_order_number



class MaintenanceRecord(models.Model):
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE, 
                              related_name='maintenance_records')
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    service_date = models.DateField()
    service_mileage = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_provider = models.ForeignKey(Supplier, on_delete=models.PROTECT, 
                                       related_name='maintenance_services')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.tire.serial_number} - {self.service_date}"

class TireWearType(models.Model):
    name = models.CharField(max_length=50)
    wear_common_cause = models.CharField(max_length=50)
    recovery_scheme = models.TextField()

    def __str__(self):
        return self.name

class TireInspection(models.Model):
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE, related_name='inspections')
    position = models.ForeignKey(TirePosition, on_delete=models.CASCADE)
    inspection_odometer = models.IntegerField()
    inspector = models.ForeignKey(Employee, on_delete=models.PROTECT, 
                                related_name='inspections')
    tread_depth = models.DecimalField(max_digits=4, decimal_places=2)
    pressure = models.DecimalField(max_digits=5, decimal_places=2)
    wear_id = models.ForeignKey(TireWearType, on_delete=models.PROTECT)

    # Fields that will be calculated in views
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
    null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.tire.last_tread_depth = self.tread_depth
        self.tire.last_pressure = self.pressure
        self.tire.save()


    def __str__(self):
        return f"{self.tire.serial_number}"



class TireAssignment(models.Model):
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE, related_name='assignments')
    tire_position_from = models.ForeignKey(TirePosition, on_delete=models.CASCADE, 
                                    related_name='assignments_from', null=True, blank=True)
    tire_position_to = models.ForeignKey(TirePosition, on_delete=models.CASCADE, 
                                  related_name='assignments_to')
    assignment_date = models.DateField()
    removal_date = models.DateField(null=True, blank=True)
    start_odometer = models.IntegerField()
    end_odometer = models.IntegerField(null=True, blank=True)
    removal_mileage = models.IntegerField(null=True, blank=True)
    reason_for_removal = models.TextField(blank=True)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, 
                                 related_name='tire_assignments')
    inspection = models.ForeignKey(TireInspection, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='assignments')
    notes = models.TextField(blank=True)

    def str(self):
        return f"{self.tire.serial_number} - {self.tire_position_to}"
    

class ImportStaging(models.Model):
    """
    Temporary storage for imported rows before database insertion
    """
    SESSION_ID = models.CharField(max_length=100, db_index=True)
    MODEL_TYPE = models.CharField(
        max_length=50,
        choices=[
            ('inventory', 'Tire Inventory'),
            ('inspection', 'Tire Inspection'),
            ('assignment', 'Tire Assignment'),
            ('maintenance', 'Maintenance Record'),
            ('custom', 'Custom'),
        ]
    )
    ROW_NUMBER = models.IntegerField()
    DATA = models.JSONField(
        default=dict,
        encoder=DjangoJSONEncoder,
        help_text="Raw row data from spreadsheet"
    )
    STATUS = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('imported', 'Imported'),
        ],
        default='pending',
        db_index=True
    )
    ERROR_MESSAGE = models.TextField(
        null=True,
        blank=True,
        help_text="Error details if import failed"
    )
    CREATED_RECORD_ID = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="ID of created database record"
    )
    CREATED_AT = models.DateTimeField(auto_now_add=True)
    UPDATED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['SESSION_ID', 'ROW_NUMBER']
        indexes = [
            models.Index(fields=['SESSION_ID', 'STATUS']),
            models.Index(fields=['MODEL_TYPE', 'STATUS']),
        ]
        verbose_name = 'Import Staging'
        verbose_name_plural = 'Import Staging'

    def __str__(self):
        return f"Row {self.ROW_NUMBER} - {self.STATUS}"


class ImportTemplate(models.Model):
    """
    Saved column mapping templates for reuse
    Allows users to save and quickly load mappings for similar spreadsheets
    """
    name = models.CharField(
        max_length=100,
        help_text="Template name (e.g., 'Inspection Report v2')"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of what this template does"
    )
    import_type = models.CharField(
        max_length=50,
        choices=[
            ('inventory', 'Tire Inventory'),
            ('inspection', 'Tire Inspection'),
            ('assignment', 'Tire Assignment'),
            ('maintenance', 'Maintenance Record'),
            ('custom', 'Custom'),
        ],
        db_index=True
    )
    mapping_rules = models.JSONField(
        default=dict,
        encoder=DjangoJSONEncoder,
        help_text="Column -> Field mapping rules"
    )
    # Example mapping_rules structure:
    # {
    #     "Serial": {"model": "Tire", "field": "serial_number", "behavior": "LOOKUP"},
    #     "TreadDepth": {"model": "TireInspection", "field": "tread_depth", "behavior": "CREATE"},
    #     "Pressure": {"model": "TireInspection", "field": "pressure", "behavior": "CREATE"},
    # }
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User who created this template"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(
        default=False,
        help_text="Allow other users to use this template"
    )
    usage_count = models.IntegerField(
        default=0,
        help_text="Number of times this template has been used"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['import_type', 'is_public']),
            models.Index(fields=['created_by', '-created_at']),
        ]
        unique_together = [('name', 'created_by')]
        verbose_name = 'Import Template'
        verbose_name_plural = 'Import Templates'

    def __str__(self):
        return f"{self.name} ({self.import_type})"


class ImportLog(models.Model):
    """
    Audit trail for all imports
    Track what was imported, when, and by whom
    """
    session_id = models.CharField(max_length=100, unique=True, db_index=True)
    import_type = models.CharField(max_length=50)
    template_used = models.ForeignKey(
        ImportTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    imported_by = models.ForeignKey(User, on_delete=models.PROTECT)
    file_name = models.CharField(max_length=255)
    total_rows = models.IntegerField()
    approved_rows = models.IntegerField()
    imported_rows = models.IntegerField()
    failed_rows = models.IntegerField()
    import_duration = models.IntegerField(
        help_text="Duration in seconds"
    )
    stats = models.JSONField(
        default=dict,
        encoder=DjangoJSONEncoder,
        help_text="Detailed statistics (records created, linked, etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['import_type', '-created_at']),
            models.Index(fields=['imported_by', '-created_at']),
        ]
        verbose_name = 'Import Log'
        verbose_name_plural = 'Import Logs'

    def __str__(self):
        return f"{self.import_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"