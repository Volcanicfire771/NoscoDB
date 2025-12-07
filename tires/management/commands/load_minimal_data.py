# tires/management/commands/load_minimal_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from tires.models import *

class Command(BaseCommand):
    help = 'Load minimal data specifically for testing tire assignment UI'

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

        self.stdout.write('Creating minimal test data for UI testing...')
        
        # ====== CRITICAL: Create the ABSOLUTE MINIMUM needed for UI ======
        
        # 1. ONE Employee (needed for WorkOrder)
        employee = Employee.objects.create(
            employment_code="TECH001",
            first_name="UI",
            last_name="Tester",
            position="Technician",
            contact_number="555-1234",
            email="tester@example.com"
        )
        
        # 2. ONE Supplier (needed for Tire)
        supplier = Supplier.objects.create(
            supplier_name="Test Supplier",
            contact_person="Test Person",
            phone="555-5678",
            position="Sales",
            email="supplier@example.com",
            address="Test Address"
        )
        
        # 3. ONE TireStatus (READY)
        status_ready = TireStatus.objects.create(
            status_name="READY",
            description="Ready for assignment"
        )
        
        status_mounted = TireStatus.objects.create(
            status_name="MOUNTED",
            description="Currently mounted"
        )
        
        # 4. ONE TirePattern
        pattern = TirePattern.objects.create(
            pattern_code="TEST-PAT",
            brand_name="Test Brand",
            country_of_origin="Test",
            load_index="121",
            speed_symbol="L",
            road_type="Highway",
            axle_type="DRIVE",
            initial_tread_depth=15.00,
            discarding_tread_depth=3.00,
            ideal_tire_pressure=100.00
        )
        
        # 5. TWO Vehicles (to test moving between vehicles)
        vehicle1 = Vehicle.objects.create(
            license_plate="VH1-001",  # Short, easy to recognize
            make="Volvo",
            year=2023,
            vehicle_type="TRUCK",
            status="ACTIVE",
            tire_configuration="6x4",
            odometer=50000,
            number_of_or_tires=6,
            number_of_sp_tires=1
        )
        
        vehicle2 = Vehicle.objects.create(
            license_plate="VH2-002",  # Short, easy to recognize
            make="Mercedes",
            year=2023,
            vehicle_type="TRUCK",
            status="ACTIVE",
            tire_configuration="6x4",
            odometer=60000,
            number_of_or_tires=6,
            number_of_sp_tires=1
        )
        
        # 6. TirePositions (2 per vehicle: 1 with tire, 1 empty)
        self.stdout.write('Creating positions (1 with tire, 1 empty per vehicle)...')
        
        # Vehicle 1 positions
        v1_pos_with_tire = TirePosition.objects.create(
            vehicle=vehicle1,
            position_name="Front Left",
            axle_number=1,
            wheel_number=1,
            axle_type="STEERING",
            tire_order=1,
            is_spare=False
        )
        
        v1_pos_empty = TirePosition.objects.create(
            vehicle=vehicle1,
            position_name="Front Right",
            axle_number=1,
            wheel_number=2,
            axle_type="STEERING",
            tire_order=2,
            is_spare=False
        )
        
        # Vehicle 2 positions
        v2_pos_with_tire = TirePosition.objects.create(
            vehicle=vehicle2,
            position_name="Front Left",
            axle_number=1,
            wheel_number=1,
            axle_type="STEERING",
            tire_order=1,
            is_spare=False
        )
        
        v2_pos_empty = TirePosition.objects.create(
            vehicle=vehicle2,
            position_name="Front Right",
            axle_number=1,
            wheel_number=2,
            axle_type="STEERING",
            tire_order=2,
            is_spare=False
        )
        
        # 7. TWO Tires (1 per vehicle, mounted)
        self.stdout.write('Creating tires (mounted on positions)...')
        
        tire1 = Tire.objects.create(
            serial_number="TIR001",  # Simple, easy to recognize
            pattern=pattern,
            status=status_mounted,
            purchase_date=timezone.now().date(),
            purchase_cost=500.00,
            supplier=supplier,
            initial_tread_depth=15.00,
            last_tread_depth=14.5,
            last_pressure=100.00,
            current_position=v1_pos_with_tire,
            current_vehicle=vehicle1
        )
        
        tire2 = Tire.objects.create(
            serial_number="TIR002",  # Simple, easy to recognize
            pattern=pattern,
            status=status_mounted,
            purchase_date=timezone.now().date(),
            purchase_cost=500.00,
            supplier=supplier,
            initial_tread_depth=15.00,
            last_tread_depth=14.0,
            last_pressure=95.00,
            current_position=v2_pos_with_tire,
            current_vehicle=vehicle2
        )
        
        # Also create 2 unmounted tires (for dropdown testing)
        tire3 = Tire.objects.create(
            serial_number="TIR003",
            pattern=pattern,
            status=status_ready,
            purchase_date=timezone.now().date(),
            purchase_cost=450.00,
            supplier=supplier,
            initial_tread_depth=16.00
        )
        
        tire4 = Tire.objects.create(
            serial_number="TIR004",
            pattern=pattern,
            status=status_ready,
            purchase_date=timezone.now().date(),
            purchase_cost=450.00,
            supplier=supplier,
            initial_tread_depth=16.00
        )
        
        # Mount the tires to positions
        v1_pos_with_tire.mounted_tire = tire1
        v1_pos_with_tire.save()
        
        v2_pos_with_tire.mounted_tire = tire2
        v2_pos_with_tire.save()
        
        # 8. WorkOrders (CRITICAL: Must have OPENED status)
        self.stdout.write('Creating work orders (OPENED status)...')
        
        # OPENED work orders (for UI testing)
        wo1 = WorkOrder.objects.create(
            work_order_number="WO001",  # Simple
            driver_id="DRV001",
            assigned_to=employee,
            vehicle=vehicle1,
            current_odometer=50000,
            shift_type="ASSIGNMENT",
            status="OPENED",  # MUST BE OPENED!
            cost=100.00,
            notes="Open work order for vehicle 1"
        )
        
        wo2 = WorkOrder.objects.create(
            work_order_number="WO002",
            driver_id="DRV002",
            assigned_to=employee,
            vehicle=vehicle2,
            current_odometer=60000,
            shift_type="ASSIGNMENT",
            status="OPENED",  # MUST BE OPENED!
            cost=120.00,
            notes="Open work order for vehicle 2"
        )
        
        # Also create a CLOSED work order (to test validation)
        wo3 = WorkOrder.objects.create(
            work_order_number="WO003",
            driver_id="DRV003",
            assigned_to=employee,
            vehicle=vehicle1,
            current_odometer=55000,
            shift_type="ASSIGNMENT",
            status="CLOSED",  # CLOSED - should not appear in dropdown
            cost=80.00,
            notes="Closed work order (should not be usable)"
        )
        
        # 9. ONE TireWearType (needed for inspection)
        wear_type = TireWearType.objects.create(
            name="Even Wear",
            wear_common_cause="Normal usage",
            recovery_scheme="Continue regular maintenance"
        )
        
        # 10. ONE TireInspection (optional field)
        inspection = TireInspection.objects.create(
            tire=tire1,
            position=v1_pos_with_tire,
            inspection_odometer=48000,
            inspector=employee,
            tread_depth=14.5,
            pressure=100.00,
            wear_id=wear_type,
            work_order=wo1
        )
        
        # 11. ONE existing TireAssignment (to show in table)
        assignment = TireAssignment.objects.create(
            tire=tire1,
            tire_position_from=None,  # Initial mounting
            tire_position_to=v1_pos_with_tire,
            assignment_date=timezone.now().date(),
            work_order=wo1,
            inspection=inspection,
            notes="Initial mounting for testing"
        )
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('MINIMAL TEST DATA CREATED FOR UI TESTING'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        # Print test scenarios
        self.stdout.write('\n=== TEST SCENARIOS ===')
        self.stdout.write('\nSCENARIO 1: Move tire within same vehicle')
        self.stdout.write(f'  From Vehicle: {vehicle1.license_plate}')
        self.stdout.write(f'  From Position: {v1_pos_with_tire.position_name} (has {tire1.serial_number})')
        self.stdout.write(f'  To Position: {v1_pos_empty.position_name} (EMPTY)')
        self.stdout.write(f'  Work Order: {wo1.work_order_number} (OPENED)')
        
        self.stdout.write('\nSCENARIO 2: Move tire between different vehicles')
        self.stdout.write(f'  From Vehicle: {vehicle1.license_plate}')
        self.stdout.write(f'  From Position: {v1_pos_with_tire.position_name} (has {tire1.serial_number})')
        self.stdout.write(f'  To Vehicle: {vehicle2.license_plate}')
        self.stdout.write(f'  To Position: {v2_pos_empty.position_name} (EMPTY)')
        self.stdout.write(f'  Work Order: {wo1.work_order_number} (OPENED)')
        
        self.stdout.write('\nSCENARIO 3: Test validation errors')
        self.stdout.write(f'  Try using CLOSED work order: {wo3.work_order_number}')
        self.stdout.write(f'  Try moving to occupied position: {v2_pos_with_tire.position_name}')
        
        self.stdout.write('\n=== DROPDOWN EXPECTATIONS ===')
        self.stdout.write(f'Vehicles dropdown: {vehicle1.license_plate}, {vehicle2.license_plate}')
        self.stdout.write(f'From Positions (after selecting vehicle): Should show positions WITH tires')
        self.stdout.write(f'To Positions (after selecting vehicle): Should show EMPTY positions')
        self.stdout.write(f'Work Orders: Should show ONLY {wo1.work_order_number} and {wo2.work_order_number} (OPENED)')
        
        self.stdout.write('\n=== VERIFY IN ADMIN ===')
        self.stdout.write('1. Check Vehicles: Should see VH1-001 and VH2-002')
        self.stdout.write('2. Check Tires: TIR001 and TIR002 should have current_position set')
        self.stdout.write('3. Check Positions: 2 positions per vehicle, 1 with tire, 1 empty')
        self.stdout.write('4. Check Work Orders: WO001 and WO002 = OPENED, WO003 = CLOSED')