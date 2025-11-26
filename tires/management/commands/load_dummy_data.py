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

        # 1. TireStatus - Create 5 statuses
        self.stdout.write('Creating TireStatus...')
        status_active = TireStatus.objects.create(
            status_name="Active",
            description="Tire is currently in use"
        )
        status_inactive = TireStatus.objects.create(
            status_name="Inactive",
            description="Tire is not in use"
        )
        status_repair = TireStatus.objects.create(
            status_name="Under Repair",
            description="Tire is being repaired"
        )
        status_scrap = TireStatus.objects.create(
            status_name="Scrap",
            description="Tire is no longer usable"
        )
        status_reserve = TireStatus.objects.create(
            status_name="Reserve",
            description="Tire is kept as backup"
        )

        # 2. TirePattern - Create 5 patterns
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
        pattern_bridgestone = TirePattern.objects.create(
            pattern_code="BST-R284",
            brand_name="Bridgestone",
            country_of_origin="Japan",
            load_index="148/145",
            speed_symbol="M",
            road_type="Mixed",
            axle_type="STEERING",
            initial_tread_depth=16.00,
            discarding_tread_depth=3.00,
            ideal_tire_pressure=110.00
        )
        pattern_goodyear = TirePattern.objects.create(
            pattern_code="GYD-UNI1",
            brand_name="Goodyear",
            country_of_origin="USA",
            load_index="150/146",
            speed_symbol="K",
            road_type="Off-road",
            axle_type="DRIVE",
            initial_tread_depth=18.00,
            discarding_tread_depth=4.00,
            ideal_tire_pressure=95.00
        )
        pattern_continental = TirePattern.objects.create(
            pattern_code="CON-HSR2",
            brand_name="Continental",
            country_of_origin="Germany",
            load_index="144/141",
            speed_symbol="L",
            road_type="Highway",
            axle_type="TRAILER",
            initial_tread_depth=14.00,
            discarding_tread_depth=2.50,
            ideal_tire_pressure=100.00
        )
        pattern_pirelli = TirePattern.objects.create(
            pattern_code="PIR-FR12",
            brand_name="Pirelli",
            country_of_origin="Italy",
            load_index="149/145",
            speed_symbol="M",
            road_type="Urban",
            axle_type="LIFTABLE",
            initial_tread_depth=15.50,
            discarding_tread_depth=3.20,
            ideal_tire_pressure=108.00
        )

        # 3. ServiceType - Create 5 service types
        self.stdout.write('Creating ServiceType...')
        service_repair = ServiceType.objects.create(
            service_name="Tire Repair",
            description="Repair of punctured or damaged tires"
        )
        service_rotation = ServiceType.objects.create(
            service_name="Tire Rotation",
            description="Rotating tires to ensure even wear"
        )
        service_balance = ServiceType.objects.create(
            service_name="Wheel Balancing",
            description="Balancing wheels for smooth operation"
        )
        service_alignment = ServiceType.objects.create(
            service_name="Wheel Alignment",
            description="Aligning wheels for proper handling"
        )
        service_inspection = ServiceType.objects.create(
            service_name="Tire Inspection",
            description="Comprehensive tire condition check"
        )

        # 4. Employee - Create 5 employees
        self.stdout.write('Creating Employee...')
        employee_john = Employee.objects.create(
            employment_code="EMP001",
            first_name="John",
            last_name="Smith",
            position="Tire Technician",
            contact_number="+1-555-0101",
            email="john.smith@company.com"
        )
        employee_mike = Employee.objects.create(
            employment_code="EMP002",
            first_name="Mike",
            last_name="Johnson",
            position="Senior Technician",
            contact_number="+1-555-0102",
            email="mike.johnson@company.com"
        )
        employee_sarah = Employee.objects.create(
            employment_code="EMP003",
            first_name="Sarah",
            last_name="Williams",
            position="Fleet Manager",
            contact_number="+1-555-0103",
            email="sarah.williams@company.com"
        )
        employee_david = Employee.objects.create(
            employment_code="EMP004",
            first_name="David",
            last_name="Brown",
            position="Maintenance Supervisor",
            contact_number="+1-555-0104",
            email="david.brown@company.com"
        )
        employee_lisa = Employee.objects.create(
            employment_code="EMP005",
            first_name="Lisa",
            last_name="Davis",
            position="Quality Inspector",
            contact_number="+1-555-0105",
            email="lisa.davis@company.com"
        )

        # 5. Supplier - Create 5 suppliers
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
        supplier_globaltires = Supplier.objects.create(
            supplier_name="Global Tires Corp.",
            contact_person="Sarah Chen",
            phone="+1-555-0203",
            position="Account Manager",
            email="sarah@globaltires.com",
            address="456 Industry Blvd, Chicago, IL 60007",
            evaluation="Premium quality tires with excellent warranty"
        )
        supplier_quickfix = Supplier.objects.create(
            supplier_name="QuickFix Services",
            contact_person="Tom Wilson",
            phone="+1-555-0204",
            position="Service Director",
            email="tom@quickfix.com",
            address="789 Service Road, Detroit, MI 48201",
            evaluation="Fast and reliable repair services"
        )
        supplier_europarts = Supplier.objects.create(
            supplier_name="EuroParts International",
            contact_person="Maria Rodriguez",
            phone="+1-555-0205",
            position="Export Manager",
            email="maria@europarts.com",
            address="321 Import Ave, Miami, FL 33101",
            evaluation="European quality parts and tires"
        )
        supplier_orientire = Supplier.objects.create(
            supplier_name="OrientiRe Distributors",
            contact_person="Kenji Tanaka",
            phone="+1-555-0206",
            position="Regional Director",
            email="kenji@orientire.com",
            address="654 Pacific Way, Los Angeles, CA 90001",
            evaluation="Competitive pricing on Asian tire brands"
        )

        # 6. Vehicle - Create 5 vehicles
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
        vehicle_trailer = Vehicle.objects.create(
            license_plate="TRL-002",
            make="Great Dane",
            year=2021,
            vehicle_type="TRAILER",
            status="ACTIVE",
            tire_configuration="11R22.5",
            odometer=75000,
            number_of_or_tires=12,
            number_of_sp_tires=1
        )
        vehicle_bus = Vehicle.objects.create(
            license_plate="BUS-003",
            make="Mercedes",
            year=2023,
            vehicle_type="BUS",
            status="ACTIVE",
            tire_configuration="275/70R22.5",
            odometer=25000,
            number_of_or_tires=6,
            number_of_sp_tires=1
        )
        vehicle_van = Vehicle.objects.create(
            license_plate="VAN-004",
            make="Ford",
            year=2022,
            vehicle_type="VAN",
            status="MAINTENANCE",
            tire_configuration="225/75R16",
            odometer=45000,
            number_of_or_tires=4,
            number_of_sp_tires=1
        )
        vehicle_truck2 = Vehicle.objects.create(
            license_plate="TRK-005",
            make="Freightliner",
            year=2020,
            vehicle_type="TRUCK",
            status="INACTIVE",
            tire_configuration="13R22.5",
            odometer=120000,
            number_of_or_tires=10,
            number_of_sp_tires=2
        )

        # 7. TirePosition - Create 5 positions per vehicle (25 total)
        self.stdout.write('Creating TirePosition...')
        positions_data = []
        
        # Vehicle 1 positions
        positions_data.extend([
            (vehicle_truck, "Front Left", 1, 1, "STEERING", 1, False),
            (vehicle_truck, "Front Right", 1, 2, "STEERING", 2, False),
            (vehicle_truck, "Rear Left Outer", 2, 1, "DRIVE", 3, False),
            (vehicle_truck, "Rear Right Outer", 2, 2, "DRIVE", 4, False),
            (vehicle_truck, "Spare", 0, 0, "STEERING", 5, True),
        ])
        
        # Vehicle 2 positions
        positions_data.extend([
            (vehicle_trailer, "Position 1", 1, 1, "TRAILER", 1, False),
            (vehicle_trailer, "Position 2", 1, 2, "TRAILER", 2, False),
            (vehicle_trailer, "Position 3", 2, 1, "TRAILER", 3, False),
            (vehicle_trailer, "Position 4", 2, 2, "TRAILER", 4, False),
            (vehicle_trailer, "Spare", 0, 0, "TRAILER", 5, True),
        ])
        
        # Vehicle 3 positions
        positions_data.extend([
            (vehicle_bus, "Front Left", 1, 1, "STEERING", 1, False),
            (vehicle_bus, "Front Right", 1, 2, "STEERING", 2, False),
            (vehicle_bus, "Middle Left", 2, 1, "DRIVE", 3, False),
            (vehicle_bus, "Middle Right", 2, 2, "DRIVE", 4, False),
            (vehicle_bus, "Spare", 0, 0, "STEERING", 5, True),
        ])
        
        # Vehicle 4 positions
        positions_data.extend([
            (vehicle_van, "Front Left", 1, 1, "STEERING", 1, False),
            (vehicle_van, "Front Right", 1, 2, "STEERING", 2, False),
            (vehicle_van, "Rear Left", 2, 1, "DRIVE", 3, False),
            (vehicle_van, "Rear Right", 2, 2, "DRIVE", 4, False),
            (vehicle_van, "Spare", 0, 0, "STEERING", 5, True),
        ])
        
        # Vehicle 5 positions
        positions_data.extend([
            (vehicle_truck2, "Front Left", 1, 1, "STEERING", 1, False),
            (vehicle_truck2, "Front Right", 1, 2, "STEERING", 2, False),
            (vehicle_truck2, "Drive Left Outer", 2, 1, "DRIVE", 3, False),
            (vehicle_truck2, "Drive Right Outer", 2, 2, "DRIVE", 4, False),
            (vehicle_truck2, "Spare", 0, 0, "STEERING", 5, True),
        ])
        
        # Create all positions
        positions = []
        for vehicle, position_name, axle, wheel, axle_type, order, is_spare in positions_data:
            pos = TirePosition.objects.create(
                vehicle=vehicle,
                position_name=position_name,
                axle_number=axle,
                wheel_number=wheel,
                axle_type=axle_type,
                tire_order=order,
                is_spare=is_spare
            )
            positions.append(pos)

        # 8. Tire - Create 25 tires (5 of each pattern)
        self.stdout.write('Creating Tire...')
        tires = []
        patterns = [pattern_michelin, pattern_bridgestone, pattern_goodyear, pattern_continental, pattern_pirelli]
        statuses = [status_active, status_active, status_active, status_inactive, status_reserve]
        suppliers = [supplier_tireworld, supplier_globaltires, supplier_europarts, supplier_orientire, supplier_quickfix]
        
        for i in range(25):
            pattern_idx = i % 5
            status_idx = i % 5
            supplier_idx = i % 5
            
            tire = Tire.objects.create(
                serial_number=f"TIR{i+1:03d}2023{patterns[pattern_idx].pattern_code[:3]}",
                pattern=patterns[pattern_idx],
                status=statuses[status_idx],
                purchase_date=timezone.now().date(),
                purchase_cost=400.00 + (i * 25),  # Varying costs
                supplier=suppliers[supplier_idx],
                initial_tread_depth=patterns[pattern_idx].initial_tread_depth,
                notes=f"Tire {i+1} - {patterns[pattern_idx].brand_name} {patterns[pattern_idx].pattern_code}"
            )
            tires.append(tire)

        # Assign some tires to positions
        for i, position in enumerate(positions[:20]):  # Assign to first 20 positions
            position.mounted_tire = tires[i]
            position.save()

        # 9. WorkOrder - Create 5 work orders
        self.stdout.write('Creating WorkOrder...')
        work_orders = []
        shift_types = ["INSPECTION", "ASSIGNMENT", "INSPECTION", "ASSIGNMENT", "INSPECTION"]
        statuses = ["PENDING", "OPENED", "COMPLETED", "CLOSED", "PENDING"]
        
        for i in range(5):
            work_order = WorkOrder.objects.create(
                work_order_number=f"WO{i+1:03d}",
                driver_id=f"DRV{i+1:03d}",
                assigned_to=[employee_john, employee_mike, employee_sarah, employee_david, employee_lisa][i],
                vehicle=[vehicle_truck, vehicle_trailer, vehicle_bus, vehicle_van, vehicle_truck2][i],
                current_odometer=50000 + (i * 10000),
                shift_type=shift_types[i],
                status=statuses[i],
                cost=75.00 + (i * 50),
                notes=f"Work order {i+1} for {['truck', 'trailer', 'bus', 'van', 'truck'][i]} maintenance"
            )
            work_orders.append(work_order)

        # 10. TireWearType - Create 5 wear types
        self.stdout.write('Creating TireWearType...')
        wear_even = TireWearType.objects.create(
            name="Even Wear",
            wear_common_cause="Normal usage",
            recovery_scheme="Continue regular maintenance and rotation"
        )
        wear_center = TireWearType.objects.create(
            name="Center Wear",
            wear_common_cause="Overinflation",
            recovery_scheme="Adjust pressure to recommended levels"
        )
        wear_edges = TireWearType.objects.create(
            name="Edge Wear",
            wear_common_cause="Underinflation",
            recovery_scheme="Increase pressure and check for leaks"
        )
        wear_shoulder = TireWearType.objects.create(
            name="Shoulder Wear",
            wear_common_cause="Cornering stress",
            recovery_scheme="Check suspension and reduce aggressive driving"
        )
        wear_patchy = TireWearType.objects.create(
            name="Patchy Wear",
            wear_common_cause="Wheel imbalance",
            recovery_scheme="Balance wheels and check suspension"
        )

        # 11. TireInspection - Create 10 inspections (2 per vehicle)
        self.stdout.write('Creating TireInspection...')
        inspections = []
        for i in range(10):
            # Use tires that are mounted on positions
            tire_idx = i % 20  # Use first 20 tires that are mounted
            vehicle_idx = i // 2  # 2 inspections per vehicle
            position_idx = i % 5  # Use different positions
            
            inspection = TireInspection.objects.create(
                tire=tires[tire_idx],
                position=positions[position_idx + (vehicle_idx * 5)],  # Positions for this vehicle
                inspection_odometer=50000 + (i * 2000),
                inspector=[employee_john, employee_mike, employee_sarah, employee_david, employee_lisa][i % 5],
                tread_depth=tires[tire_idx].initial_tread_depth - (i * 0.5),  # Simulate wear
                pressure=100.00 - (i * 2),  # Simulate pressure variation
                wear_id=[wear_even, wear_center, wear_edges, wear_shoulder, wear_patchy][i % 5],
                # Calculated fields will be set by your view logic
                consumption_rate=0.05 + (i * 0.01),
                remaining_traveling_distance=100000 - (i * 5000),
                cost_per_mm_tread_depth=25.00 + (i * 2),
                cost_per_1000_km_travel=1.50 + (i * 0.1),
                fuel_consumption_increase=0.1 + (i * 0.05),
                fuel_loss_caused=50.00 + (i * 10),
                current_tire_value=300.00 - (i * 15),
                balance_traveling_distance=80000 - (i * 4000)
            )
            inspections.append(inspection)

        # 12. TireAssignment - Create 5 assignments with updated structure
        self.stdout.write('Creating TireAssignment...')
        for i in range(5):
            # Use different tires and positions for assignments
            from_position_idx = i
            to_position_idx = (i + 2) % 20  # Assign to different position
            
            assignment = TireAssignment.objects.create(
                tire=tires[i],
                tire_position_from=positions[from_position_idx],
                tire_position_to=positions[to_position_idx],
                assignment_date=timezone.now().date(),
                removal_date=timezone.now().date() if i % 2 == 0 else None,  # Some have removal dates
                work_order=work_orders[i],
                inspection=inspections[i],  # Link to corresponding inspection
                reason_for_removal="Regular rotation" if i % 2 == 0 else "Wear issues",
                notes=f"Tire assignment {i+1} - {tires[i].serial_number} from {positions[from_position_idx].position_name} to {positions[to_position_idx].position_name}"
            )

        # 13. MaintenanceRecord - Create 5 maintenance records
        self.stdout.write('Creating MaintenanceRecord...')
        for i in range(5):
            maintenance = MaintenanceRecord.objects.create(
                vehicle=[vehicle_truck, vehicle_trailer, vehicle_bus, vehicle_van, vehicle_truck2][i],
                service_type=[service_repair, service_rotation, service_balance, service_alignment, service_inspection][i],
                service_date=timezone.now().date(),
                service_mileage=50000 + (i * 15000),
                cost=120.00 + (i * 80),
                service_provider=[supplier_tireworld, supplier_globaltires, supplier_quickfix, supplier_europarts, supplier_orientire][i],
                notes=f"Maintenance record {i+1} - {['repair', 'rotation', 'balancing', 'alignment', 'inspection'][i]} service"
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded dummy data for all models with updated TireAssignment structure!')
        )