from django.core.management.base import BaseCommand
from django.utils import timezone
from tires.models import *

class Command(BaseCommand):
    help = 'Load dummy data for all models'

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        TireInspection.objects.all().delete()
        TireAssignment.objects.all().delete()
        WorkOrder.objects.all().delete()
        Tire.objects.all().delete()
        TirePosition.objects.all().delete()
        Vehicle.objects.all().delete()
        Supplier.objects.all().delete()
        Employee.objects.all().delete()
        ServiceType.objects.all().delete()
        TirePattern.objects.all().delete()
        TireStatus.objects.all().delete()
        TireWearType.objects.all().delete()

        # 1. TireStatus
        self.stdout.write('Creating TireStatus...')
        status_active = TireStatus.objects.create(
            status_name="Active",
            description="Tire is currently in use"
        )

        # 2. TirePattern
        self.stdout.write('Creating TirePattern...')
        pattern_michelin = TirePattern.objects.create(
            pattern_code="MIC-XZA2",
            brand_name="Michelin",
            country_of_origin="France",
            load_index="152/148",
            speed_symbol="L",
            road_type="Highway",
            axle_type="DRIVE",
            initial_tread_depth=15.00,
            discarding_tread_depth=3.00,
            ideal_tire_pressure=105.00
        )

        # 3. ServiceType
        self.stdout.write('Creating ServiceType...')
        service_repair = ServiceType.objects.create(
            service_name="Tire Repair",
            description="Repair of punctured or damaged tires"
        )

        # 4. Employee
        self.stdout.write('Creating Employee...')
        employee_john = Employee.objects.create(
            employment_code="EMP001",
            first_name="John",
            last_name="Smith",
            position="Tire Technician",
            contact_number="+1-555-0101",
            email="john.smith@company.com"
        )

        # 5. Supplier
        self.stdout.write('Creating Supplier...')
        supplier_tireworld = Supplier.objects.create(
            supplier_name="TireWorld Inc.",
            contact_person="Mike Johnson",
            phone="+1-555-0202",
            position="Sales Manager",
            email="mike@tireworld.com",
            address="123 Tire Street, Industrial Park, TX 75001",
            evaluation="Reliable supplier with good pricing"
        )

        # 6. Vehicle
        self.stdout.write('Creating Vehicle...')
        vehicle_truck = Vehicle.objects.create(
            license_plate="TRK-001",
            make="Volvo",
            year=2022,
            vehicle_type="TRUCK",
            status="ACTIVE",
            tire_configuration="12R22.5",
            odometer=50000,
            number_of_or_tires=8,
            number_of_sp_tires=2
        )

        # 7. TirePosition
        self.stdout.write('Creating TirePosition...')
        position_front = TirePosition.objects.create(
            vehicle=vehicle_truck,
            position_name="Front Left",
            axle_number=1,
            wheel_number=1,
            axle_type="STEERING",
            tire_order=1,
            hounded_tire_id="FL001",
            is_spare=False
        )

        # 8. Tire
        self.stdout.write('Creating Tire...')
        tire_001 = Tire.objects.create(
            serial_number="TIR0012023XYZ",
            pattern=pattern_michelin,
            status=status_active,
            purchase_date=timezone.now().date(),
            purchase_cost=450.00,
            supplier=supplier_tireworld,
            initial_tread_depth=15.00,
            notes="New tire for front position"
        )

        # 9. WorkOrder
        self.stdout.write('Creating WorkOrder...')
        work_order = WorkOrder.objects.create(
            work_order_number="WO001",
            driver_id="DRV001",
            assigned_to=employee_john,
            vehicle=vehicle_truck,
            current_odometer=50000,
            shift_type="INSTALLATION",
            status="COMPLETED",
            cost=75.00,
            notes="Initial tire installation for new vehicle"
        )

        # 10. TireAssignment - FIXED: Added end_odometer
        self.stdout.write('Creating TireAssignment...')
        assignment_1 = TireAssignment.objects.create(
            tire=tire_001,
            to_position=position_front,
            assignment_date=timezone.now().date(),
            start_odometer=50000,
            end_odometer=50500,  # ADDED THIS - needed for PTM calculation
            work_order=work_order,
            inspector=employee_john,
            notes="Initial tire installation - Front Left"
        )

        # 11. MaintenanceRecord
        self.stdout.write('Creating MaintenanceRecord...')
        maintenance = MaintenanceRecord.objects.create(
            vehicle=vehicle_truck,
            service_type=service_repair,
            service_date=timezone.now().date(),
            service_mileage=50000,
            cost=120.00,
            service_provider=supplier_tireworld,
            notes="Routine tire inspection and pressure check"
        )

        # 12. TireWearType
        self.stdout.write('Creating TireWearType...')
        wear_even = TireWearType.objects.create(
            name="Even Wear",
            wear_common_cause="Normal usage",
            recovery_scheme="Continue regular maintenance and rotation"
        )