# tires/management/commands/create_tire_assignment_test_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from tires.models import *

class Command(BaseCommand):
    help = 'Create test data for tire assignment testing (matches exact models)'

    def handle(self, *args, **options):
        with transaction.atomic():
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

            self.stdout.write(self.style.SUCCESS('\n' + '='*70))
            self.stdout.write(self.style.SUCCESS('CREATING TIRE ASSIGNMENT TEST DATA'))
            self.stdout.write(self.style.SUCCESS('='*70))

            # ========== CREATE BASE DATA ==========
            self.stdout.write('\n1. Creating base entities...')
            
            # Create employees
            technician = Employee.objects.create(
                employment_code="TECH001",
                first_name="John",
                last_name="Technician",
                position="Senior Technician",
                contact_number="555-1001",
                email="john.tech@test.com"
            )
            
            inspector = Employee.objects.create(
                employment_code="INSP001",
                first_name="Jane",
                last_name="Inspector",
                position="Tire Inspector",
                contact_number="555-1002",
                email="jane.insp@test.com"
            )
            
            # Create supplier
            supplier = Supplier.objects.create(
                supplier_name="Test Tire Supplier",
                contact_person="Bob Supplier",
                phone="555-2001",
                position="Sales Manager",
                email="bob@testsupplier.com",
                address="123 Test Street, Test City",
                evaluation="Good supplier for testing"
            )
            
            # Create tire statuses (must match your status names)
            status_ready = TireStatus.objects.create(
                status_name="READY",
                description="Ready for mounting"
            )
            
            status_mounted = TireStatus.objects.create(
                status_name="MOUNTED",
                description="Currently mounted on vehicle"
            )
            
            status_discarded = TireStatus.objects.create(
                status_name="DISCARDED",
                description="Tire has been discarded"
            )
            
            # Create tire patterns
            pattern_steer = TirePattern.objects.create(
                pattern_code="PAT-STEER-001",
                brand_name="TestSteer",
                country_of_origin="Testland",
                load_index="121",
                speed_symbol="L",
                road_type="Highway",
                axle_type="STEERING",
                initial_tread_depth=16.00,
                discarding_tread_depth=3.00,
                ideal_tire_pressure=105.00
            )
            
            pattern_drive = TirePattern.objects.create(
                pattern_code="PAT-DRIVE-001",
                brand_name="TestDrive",
                country_of_origin="Testland",
                load_index="125",
                speed_symbol="L",
                road_type="Highway",
                axle_type="DRIVE",
                initial_tread_depth=18.00,
                discarding_tread_depth=3.00,
                ideal_tire_pressure=110.00
            )
            
            # ========== CREATE VEHICLES ==========
            self.stdout.write('\n2. Creating vehicles...')
            
            vehicle1 = Vehicle.objects.create(
                license_plate="VH-001",
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
                license_plate="VH-002",
                make="Mercedes",
                year=2023,
                vehicle_type="TRUCK",
                status="ACTIVE",
                tire_configuration="6x4",
                odometer=60000,
                number_of_or_tires=6,
                number_of_sp_tires=1
            )
            
            self.stdout.write(f'  Created: {vehicle1.license_plate} ({vehicle1.make})')
            self.stdout.write(f'  Created: {vehicle2.license_plate} ({vehicle2.make})')
            
            # ========== CREATE TIRE POSITIONS ==========
            self.stdout.write('\n3. Creating tire positions...')
            
            # Vehicle 1 positions: 2 with tires, 2 empty
            v1_pos_with_tire1 = TirePosition.objects.create(
                vehicle=vehicle1,
                position_name="Front Left",
                axle_number=1,
                wheel_number=1,
                axle_type="STEERING",
                tire_order=1,
                is_spare=False
            )
            
            v1_pos_with_tire2 = TirePosition.objects.create(
                vehicle=vehicle1,
                position_name="Front Right",
                axle_number=1,
                wheel_number=2,
                axle_type="STEERING",
                tire_order=2,
                is_spare=False
            )
            
            v1_pos_empty1 = TirePosition.objects.create(
                vehicle=vehicle1,
                position_name="Drive Left 1",
                axle_number=2,
                wheel_number=1,
                axle_type="DRIVE",
                tire_order=3,
                is_spare=False
            )
            
            v1_pos_empty2 = TirePosition.objects.create(
                vehicle=vehicle1,
                position_name="Drive Right 1",
                axle_number=2,
                wheel_number=2,
                axle_type="DRIVE",
                tire_order=4,
                is_spare=False
            )
            
            # Vehicle 2 positions: 2 with tires, 2 empty
            v2_pos_with_tire1 = TirePosition.objects.create(
                vehicle=vehicle2,
                position_name="Front Left",
                axle_number=1,
                wheel_number=1,
                axle_type="STEERING",
                tire_order=1,
                is_spare=False
            )
            
            v2_pos_with_tire2 = TirePosition.objects.create(
                vehicle=vehicle2,
                position_name="Front Right",
                axle_number=1,
                wheel_number=2,
                axle_type="STEERING",
                tire_order=2,
                is_spare=False
            )
            
            v2_pos_empty1 = TirePosition.objects.create(
                vehicle=vehicle2,
                position_name="Drive Left 1",
                axle_number=2,
                wheel_number=1,
                axle_type="DRIVE",
                tire_order=3,
                is_spare=False
            )
            
            v2_pos_empty2 = TirePosition.objects.create(
                vehicle=vehicle2,
                position_name="Drive Right 1",
                axle_number=2,
                wheel_number=2,
                axle_type="DRIVE",
                tire_order=4,
                is_spare=False
            )
            
            self.stdout.write(f'  Created {TirePosition.objects.count()} positions total')
            self.stdout.write(f'  - Vehicle 1: 2 positions with tires, 2 empty positions')
            self.stdout.write(f'  - Vehicle 2: 2 positions with tires, 2 empty positions')
            
            # ========== CREATE TIRES ==========
            self.stdout.write('\n4. Creating tires...')
            
            # Mounted tires for Vehicle 1
            tire1 = Tire.objects.create(
                serial_number="TIR-001",
                pattern=pattern_steer,
                status=status_mounted,
                purchase_date=timezone.now().date(),
                purchase_cost=550.00,
                supplier=supplier,
                initial_tread_depth=16.00,
                last_tread_depth=15.50,
                last_pressure=105.00,
                current_position=v1_pos_with_tire1,
                current_vehicle=vehicle1
            )
            v1_pos_with_tire1.mounted_tire = tire1
            v1_pos_with_tire1.save()
            
            tire2 = Tire.objects.create(
                serial_number="TIR-002",
                pattern=pattern_drive,
                status=status_mounted,
                purchase_date=timezone.now().date(),
                purchase_cost=600.00,
                supplier=supplier,
                initial_tread_depth=18.00,
                last_tread_depth=17.00,
                last_pressure=110.00,
                current_position=v1_pos_with_tire2,
                current_vehicle=vehicle1
            )
            v1_pos_with_tire2.mounted_tire = tire2
            v1_pos_with_tire2.save()
            
            # Mounted tires for Vehicle 2
            tire3 = Tire.objects.create(
                serial_number="TIR-003",
                pattern=pattern_steer,
                status=status_mounted,
                purchase_date=timezone.now().date(),
                purchase_cost=550.00,
                supplier=supplier,
                initial_tread_depth=16.00,
                last_tread_depth=14.50,
                last_pressure=103.00,
                current_position=v2_pos_with_tire1,
                current_vehicle=vehicle2
            )
            v2_pos_with_tire1.mounted_tire = tire3
            v2_pos_with_tire1.save()
            
            tire4 = Tire.objects.create(
                serial_number="TIR-004",
                pattern=pattern_drive,
                status=status_mounted,
                purchase_date=timezone.now().date(),
                purchase_cost=600.00,
                supplier=supplier,
                initial_tread_depth=18.00,
                last_tread_depth=16.00,
                last_pressure=108.00,
                current_position=v2_pos_with_tire2,
                current_vehicle=vehicle2
            )
            v2_pos_with_tire2.mounted_tire = tire4
            v2_pos_with_tire2.save()
            
            # Unmounted tires (READY status)
            tire5 = Tire.objects.create(
                serial_number="UNM-001",
                pattern=pattern_steer,
                status=status_ready,
                purchase_date=timezone.now().date(),
                purchase_cost=500.00,
                supplier=supplier,
                initial_tread_depth=16.00,
                current_position=None,
                current_vehicle=None
            )
            
            tire6 = Tire.objects.create(
                serial_number="UNM-002",
                pattern=pattern_drive,
                status=status_ready,
                purchase_date=timezone.now().date(),
                purchase_cost=525.00,
                supplier=supplier,
                initial_tread_depth=18.00,
                current_position=None,
                current_vehicle=None
            )
            
            tire7 = Tire.objects.create(
                serial_number="UNM-003",
                pattern=pattern_steer,
                status=status_ready,
                purchase_date=timezone.now().date(),
                purchase_cost=500.00,
                supplier=supplier,
                initial_tread_depth=16.00,
                current_position=None,
                current_vehicle=None
            )
            
            # One scrapped tire
            tire8 = Tire.objects.create(
                serial_number="SCR-001",
                pattern=pattern_drive,
                status=status_discarded,
                purchase_date=timezone.now().date(),
                purchase_cost=650.00,
                supplier=supplier,
                initial_tread_depth=2.50,
                last_tread_depth=2.50,
                last_pressure=0.00,
                is_scrapped=True,
                current_position=None,
                current_vehicle=None
            )
            
            self.stdout.write(f'  Created {Tire.objects.count()} tires total:')
            self.stdout.write(f'    - Mounted on vehicles: TIR-001, TIR-002, TIR-003, TIR-004')
            self.stdout.write(f'    - Unmounted (READY): UNM-001, UNM-002, UNM-003')
            self.stdout.write(f'    - Scrapped: SCR-001')
            
            # ========== CREATE WORK ORDERS ==========
            self.stdout.write('\n5. Creating work orders...')
            
            # OPENED work orders (these should appear in dropdown)
            wo1 = WorkOrder.objects.create(
                work_order_number="WO-001",
                driver_id="DRV-001",
                assigned_to=technician,
                vehicle=vehicle1,
                current_odometer=50000,
                shift_type="ASSIGNMENT",
                status="OPENED",
                cost=150.00,
                notes="Open work order for VH-001"
            )
            
            wo2 = WorkOrder.objects.create(
                work_order_number="WO-002",
                driver_id="DRV-002",
                assigned_to=technician,
                vehicle=vehicle2,
                current_odometer=60000,
                shift_type="ASSIGNMENT",
                status="OPENED",
                cost=180.00,
                notes="Open work order for VH-002"
            )
            
            # One CLOSED work order (should NOT appear in dropdown)
            WorkOrder.objects.create(
                work_order_number="WO-999",
                driver_id="DRV-999",
                assigned_to=technician,
                vehicle=vehicle1,
                current_odometer=55000,
                shift_type="ASSIGNMENT",
                status="CLOSED",
                cost=120.00,
                notes="Closed work order (should not appear)"
            )
            
            self.stdout.write(f'  Created work orders:')
            self.stdout.write(f'    - OPENED: WO-001 (for VH-001), WO-002 (for VH-002)')
            self.stdout.write(f'    - CLOSED: WO-999 (should NOT appear in dropdown)')
            
            # ========== CREATE TIRE WEAR TYPES ==========
            self.stdout.write('\n6. Creating wear types...')
            
            wear_type1 = TireWearType.objects.create(
                name="Even Wear",
                wear_common_cause="Normal usage",
                recovery_scheme="Continue regular maintenance"
            )
            
            wear_type2 = TireWearType.objects.create(
                name="Center Wear",
                wear_common_cause="Overinflation",
                recovery_scheme="Adjust pressure to recommended level"
            )
            
            # ========== CREATE INSPECTIONS ==========
            self.stdout.write('\n7. Creating inspections...')
            
            # Create inspection for TIR-001
            inspection1 = TireInspection.objects.create(
                tire=tire1,
                position=v1_pos_with_tire1,
                inspection_odometer=48000,
                inspector=inspector,
                tread_depth=15.50,
                pressure=105.00,
                wear_id=wear_type1,
                work_order=wo1
            )
            
            # Create inspection for TIR-003
            inspection2 = TireInspection.objects.create(
                tire=tire3,
                position=v2_pos_with_tire1,
                inspection_odometer=58000,
                inspector=inspector,
                tread_depth=14.50,
                pressure=103.00,
                wear_id=wear_type2,
                work_order=wo2
            )
            
            self.stdout.write(f'  Created {TireInspection.objects.count()} inspections')
            self.stdout.write(f'    - For TIR-001 (on VH-001 Front Left)')
            self.stdout.write(f'    - For TIR-003 (on VH-002 Front Left)')
            
            # ========== CREATE SAMPLE ASSIGNMENTS ==========
            self.stdout.write('\n8. Creating sample assignments for table...')
            
            # Sample 1: Normal move (no discard flag)
            assignment1 = TireAssignment.objects.create(
                tire=tire1,
                tire_position_from=None,
                tire_position_to=v1_pos_with_tire1,
                assignment_date=timezone.now().date(),
                work_order=wo1,
                inspection=inspection1,
                reason_for_removal="",
                notes="Initial mounting"
            )
            
            # Sample 2: New mount (no extra flag - template uses from_position_is_new_mount which doesn't exist)
            assignment2 = TireAssignment.objects.create(
                tire=tire5,
                tire_position_from=None,
                tire_position_to=v1_pos_empty1,
                assignment_date=timezone.now().date(),
                work_order=wo1,
                inspection=None,
                reason_for_removal="",
                notes="Mounted new tire"
            )
            
            # Sample 3: Discard operation
            assignment3 = TireAssignment.objects.create(
                tire=tire3,
                tire_position_from=v2_pos_with_tire1,
                tire_position_to=None,  # Null for discard
                assignment_date=timezone.now().date(),
                work_order=wo2,
                inspection=inspection2,
                reason_for_removal="Worn beyond safe limits",
                notes="Discarded tire",
                is_discard_operation=True  # This field exists in your model
            )
            
            # For the discard, also update the tire
            tire3.status = status_discarded
            tire3.is_scrapped = True
            tire3.current_position = None
            tire3.current_vehicle = None
            tire3.save()
            v2_pos_with_tire1.mounted_tire = None
            v2_pos_with_tire1.save()
            
            self.stdout.write(f'  Created {TireAssignment.objects.count()} sample assignments')
            
            # ========== PRINT TESTING GUIDE ==========
            self.stdout.write(self.style.SUCCESS('\n' + '='*70))
            self.stdout.write(self.style.SUCCESS('TEST DATA CREATION COMPLETE!'))
            self.stdout.write(self.style.SUCCESS('='*70))
            
            self.stdout.write('\n' + '='*70)
            self.stdout.write('QUICK TEST GUIDE')
            self.stdout.write('='*70)
            
            self.stdout.write('\n1. TEST "MOVE TIRE" OPERATION:')
            self.stdout.write('   - Click "🔄 Move Tire" button')
            self.stdout.write('   - From Vehicle: VH-001')
            self.stdout.write('   - From Position: Front Left (TIR-001) or Front Right (TIR-002)')
            self.stdout.write('   - To Vehicle: VH-002')
            self.stdout.write('   - To Position: Drive Left 1 (EMPTY) or Drive Right 1 (EMPTY)')
            self.stdout.write('   - Work Order: WO-001')
            self.stdout.write('   - Submit')
            
            self.stdout.write('\n2. TEST "MOUNT NEW" OPERATION:')
            self.stdout.write('   - Click "🆕 Mount New" button')
            self.stdout.write('   - Select unmounted tire: UNM-001, UNM-002, or UNM-003')
            self.stdout.write('   - To Vehicle: VH-001 or VH-002')
            self.stdout.write('   - To Position: Any empty position (Drive Left 1, Drive Right 1)')
            self.stdout.write('   - Work Order: WO-001 (for VH-001) or WO-002 (for VH-002)')
            self.stdout.write('   - Submit')
            
            self.stdout.write('\n3. TEST "DISCARD TIRE" OPERATION:')
            self.stdout.write('   - Click "🚫 Discard Tire" button')
            self.stdout.write('   - From Vehicle: VH-001 or VH-002')
            self.stdout.write('   - From Position: Front Left or Front Right (has tire)')
            self.stdout.write('   - Reason: Enter any reason')
            self.stdout.write('   - Work Order: WO-001 (for VH-001) or WO-002 (for VH-002)')
            self.stdout.write('   - Submit (will ask for confirmation)')
            
            self.stdout.write('\n4. TEST VALIDATION ERRORS:')
            self.stdout.write('   - Try to mount SCR-001 (scrapped tire) - should fail')
            self.stdout.write('   - Try to move to occupied position - should fail')
            self.stdout.write('   - Try discard without reason - should fail')
            
            self.stdout.write('\n' + '='*70)
            self.stdout.write('DATA SUMMARY')
            self.stdout.write('='*70)
            
            self.stdout.write(f'\nVehicles: 2')
            self.stdout.write(f'  VH-001 (Volvo) - 4 positions (2 with tires, 2 empty)')
            self.stdout.write(f'  VH-002 (Mercedes) - 4 positions (2 with tires, 2 empty)')
            
            self.stdout.write(f'\nTires: {Tire.objects.count()}')
            self.stdout.write(f'  Mounted: TIR-001, TIR-002 (on VH-001), TIR-003, TIR-004 (on VH-002)')
            self.stdout.write(f'  Unmounted (READY): UNM-001, UNM-002, UNM-003')
            self.stdout.write(f'  Scrapped: SCR-001')
            
            self.stdout.write(f'\nWork Orders: {WorkOrder.objects.count()}')
            self.stdout.write(f'  OPENED: WO-001 (for VH-001), WO-002 (for VH-002)')
            self.stdout.write(f'  CLOSED: WO-999 (not in dropdown)')
            
            self.stdout.write(f'\nSample Assignments in table: {TireAssignment.objects.count()}')
            self.stdout.write(f'  (1 normal move, 1 new mount, 1 discard)')
            
            self.stdout.write('\n' + '='*70)
            self.stdout.write(self.style.SUCCESS('RUN COMMAND:'))
            self.stdout.write(self.style.SUCCESS('python manage.py create_tire_assignment_test_data'))
            self.stdout.write('='*70)