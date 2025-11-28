from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import TireInspection, Tire, TirePosition, Employee, TireWearType, Vehicle, WorkOrder, TireAssignment
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Tire Inspections Views ------------------------------------------------------------------------------------------------------

def tire_inspections_list(request):
    # Start with all records
    tire_inspections = TireInspection.objects.all()
    tires = Tire.objects.all()
    tire_positions = TirePosition.objects.all()
    employees = Employee.objects.all()
    wear_types = TireWearType.objects.all()
    vehicles = Vehicle.objects.all()

    # Fix vehicle_tire_data to be JSON serializable
    vehicle_tire_data = {}
    for vehicle in vehicles:
        vehicle_positions = TirePosition.objects.filter(vehicle=vehicle)
        tires_list = []
        for pos in vehicle_positions:
            if pos.mounted_tire:
                tire = pos.mounted_tire
                # Get latest inspection data
                latest_inspection = TireInspection.objects.filter(
                    tire=tire
                ).order_by('-id').first()
                
                tires_list.append({
                    "tire_id": str(tire.id),  # Convert to string
                    "serial": str(tire.serial_number),  # Convert to string
                    "tread": float(latest_inspection.tread_depth) if latest_inspection else 0.0,
                    "pressure": float(latest_inspection.pressure) if latest_inspection else 0.0,
                    "position": str(pos.position_name)  # Convert to string
                })
        vehicle_tire_data[str(vehicle.id)] = tires_list  # Use string keys

    # Get filter parameters from request
    tire_filter = request.GET.get('tire_filter', '')
    axle_type_filter = request.GET.get('axle_type_filter', '')
    inspector_filter = request.GET.get('inspector_filter', '')
    wear_filter = request.GET.get('wear_filter', '')
    work_order_id = request.GET.get('work_order', '')
    
    # Initialize variables with default values
    vehicle_filter = None
    employee_filter = None
    inspection_odometer_autofill = None
    work_order_obj = None
    tire_position_map = {}

    # Only try to get work order if work_order_id exists and is not empty
    if work_order_id:
        try:
            work_order_obj = WorkOrder.objects.get(id=work_order_id)
            inspection_odometer_autofill = work_order_obj.current_odometer
            vehicle_filter = work_order_obj.vehicle.id
            employee_filter = work_order_obj.assigned_to
        except (WorkOrder.DoesNotExist, ValueError):
            # Handle invalid work order ID gracefully
            pass
    
    # Apply filters only if they exist
    if tire_filter:
        tire_inspections = tire_inspections.filter(tire_id=tire_filter)
    if axle_type_filter:
        tire_inspections = tire_inspections.filter(position__axle_type=axle_type_filter)  
    if inspector_filter:
        tire_inspections = tire_inspections.filter(inspector_id=inspector_filter)
    if wear_filter:
        tire_inspections = tire_inspections.filter(wear_id=wear_filter)  

    # Handle vehicle-based filtering
    if vehicle_filter:
        # Get all tire positions for this vehicle
        vehicle_positions = TirePosition.objects.filter(vehicle_id=vehicle_filter)
        
        # Get tires that are currently mounted on these positions
        mounted_tire_ids = vehicle_positions.exclude(
            mounted_tire__isnull=True
        ).values_list('mounted_tire_id', flat=True)
        
        # Filter tires to show only those mounted on this vehicle
        tires = Tire.objects.filter(id__in=mounted_tire_ids)
        
        # Create a dictionary mapping tire IDs to their positions
        for position in vehicle_positions:
            if position.mounted_tire:
                tire_position_map[str(position.mounted_tire.id)] = str(position.id)  # Convert to strings
    else:
        vehicle_positions = TirePosition.objects.all()

    # Fix tire_position_map to use string keys and values
    tire_position_map_json = {}
    for tire_id, position_id in tire_position_map.items():
        tire_position_map_json[str(tire_id)] = str(position_id)

    context = {
        'tire_inspections': tire_inspections,
        'tires': tires,
        'tire_positions': vehicle_positions,
        'employees': employees,
        'wear_types': wear_types,
        'tire_filter': tire_filter,
        'axle_type_filter': axle_type_filter, 
        'inspector_filter': inspector_filter,
        'wear_filter': wear_filter,
        'vehicle_filter': vehicle_filter,  
        'work_order': work_order_id,
        'employee_filter': employee_filter,
        'tire_position_map': tire_position_map_json,  # Use the JSON-safe version
        'inspection_odometer': inspection_odometer_autofill,
        'work_order_obj': work_order_obj,
        'vehicles': vehicles,
        'vehicle_tire_data': vehicle_tire_data,
    }
    return render(request, 'tire_inspections/tire_inspections_list.html', context)



@csrf_exempt
def bulk_tire_update(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        vehicle_id = request.POST.get("vehicle_id")
        work_order_id = request.POST.get("work_order_id")
        inspector_id = request.POST.get("inspector_id")
        odometer = request.POST.get("odometer")

        print(f"Bulk update received - Vehicle: {vehicle_id}, Work Order: {work_order_id}")

        # Get related objects
        work_order = WorkOrder.objects.get(id=work_order_id) if work_order_id else None
        inspector = Employee.objects.get(id=inspector_id) if inspector_id else None
        vehicle = Vehicle.objects.get(id=vehicle_id) if vehicle_id else None
        
        # -------------------------------
        # NEW: COST + CLOSE WORK ORDER
        # -------------------------------
        cost_value = request.POST.get("cost")
        close_flag = request.POST.get("close_work_order")
        print(f"Cost: {cost_value}\t flag: {close_flag}")
        if work_order:
            if cost_value:
                work_order.cost = cost_value

            if close_flag == "on":
                work_order.status = "CLOSED"

            work_order.save()
        # -------------------------------
        
        # Get default wear type
        default_wear_type = TireWearType.objects.first()
        
        created_inspections = 0
        
        # Get all positions for this vehicle
        vehicle_positions = TirePosition.objects.filter(vehicle=vehicle)
        
        for position in vehicle_positions:
            if position.mounted_tire:
                tire = position.mounted_tire

                # Get the updated values from the form
                new_tread = request.POST.get(f"tire_{tire.id}_new_tread")
                new_pressure = request.POST.get(f"tire_{tire.id}_new_pressure")
                
                # Only create inspection if both values are provided
                if new_tread and new_pressure:
                    inspection = TireInspection.objects.create(
                        tire=tire,
                        position=position,
                        inspection_odometer=odometer,
                        inspector=inspector,
                        tread_depth=new_tread,
                        pressure=new_pressure,
                        wear_id=default_wear_type,
                        work_order=work_order
                    )

                    # Default calculation placeholders
                    inspection.consumption_rate = 0
                    inspection.remaining_traveling_distance = 0
                    inspection.cost_per_mm_tread_depth = 0
                    inspection.cost_per_1000_km_travel = 0
                    inspection.fuel_consumption_increase = 0
                    inspection.fuel_loss_caused = 0
                    inspection.current_tire_value = 0
                    inspection.balance_traveling_distance = 0
                    inspection.save()
                    
                    created_inspections += 1
                    print(f"Created inspection for tire {tire.serial_number} at position {position.position_name}")

        return JsonResponse({
            "status": "success", 
            "message": f"Created {created_inspections} tire inspections successfully"
        })

    except Exception as e:
        print(f"Error in bulk_tire_update: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

def tire_inspections_delete(request, id):
    if request.method == 'POST':
        tire_inspection = TireInspection.objects.get(id=id)
        tire_inspection.delete()
        messages.success(request, 'Tire inspection deleted successfully!')
    return redirect('tire_inspections_list')

def tire_inspections_create(request):
    if request.method == 'POST':
        # Get data from the form
        tire_id = request.POST.get('tire')
        position_id = request.POST.get('position')
        inspection_odometer = request.POST.get('inspection_odometer')
        inspector_id = request.POST.get('inspector')
        tread_depth = request.POST.get('tread_depth')
        CTP = float(request.POST.get('pressure'))  # Convert to float
        wear_id = request.POST.get('wear_id')
        tire = Tire.objects.get(id=tire_id)
        position = TirePosition.objects.get(id=position_id)
        inspector = Employee.objects.get(id=inspector_id)
        wear_type = TireWearType.objects.get(id=wear_id)
        # tire_assignment = TireAssignment.objects.get(tire=tire)

        # Current values from this inspection
        CTD = float(tread_depth)  # Current Tread Depth
        CTO = int(inspection_odometer)  # Current Odometer
        DTD = float(tire.pattern.discarding_tread_depth)  # Discarding Tread Depth
        TPP = float(tire.purchase_cost)  # Tire Purchase Price
        ITD = float(tire.pattern.initial_tread_depth)  # Initial Tread Depth
        ITP = float(tire.pattern.ideal_tire_pressure)  # Ideal Tire Pressure
        # PTM = tire_assignment.end_odometer - tire_assignment.start_odometer  # Position Tire Mileage

        # # DEBUG: Print all input values
        # print("=== DEBUG INPUT VALUES ===")
        # print(f"CTD (Current Tread Depth): {CTD}")
        # print(f"CTO (Current Odometer): {CTO}")
        # print(f"DTD (Discarding Tread Depth): {DTD}")
        # print(f"TPP (Tire Purchase Price): {TPP}")
        # print(f"ITD (Initial Tread Depth): {ITD}")
        # print(f"ITP (Ideal Tire Pressure): {ITP}")
        # print(f"CTP (Current Tire Pressure): {CTP}")
        # print(f"PTM (Position Tire Mileage): {PTM}")

        # Find the most recent previous inspection for this tire
        previous_inspection = TireInspection.objects.filter(
            tire=tire
        ).order_by('-inspection_odometer').first()
        
        if previous_inspection:
            # Use previous inspection data
            PTD = float(previous_inspection.tread_depth)  # Previous Tread Depth
            PTO = previous_inspection.inspection_odometer  # Previous Odometer
            # print(f"PREVIOUS INSPECTION FOUND:")
            # print(f"PTD (Previous Tread Depth): {PTD}")
            # print(f"PTO (Previous Odometer): {PTO}")
        else:
            # First inspection - use initial values
            PTD = ITD  # From pattern
            # Get odometer from first assignment
            first_assignment = tire.assignments.order_by('assignment_date').first()
            PTO = first_assignment.start_odometer if first_assignment else 0
            # print(f"NO PREVIOUS INSPECTION - USING INITIAL VALUES:")
            # print(f"PTD (Using Initial Tread Depth): {PTD}")
            # print(f"PTO (Using Assignment Start): {PTO}")

        # Calculate consumption rate (CRP)
        # print(f"Calculating CRP: (({PTD} - {CTD}) * 10000) / ({CTO} - {PTO})")
        if CTO > PTO and PTD > CTD:
            CRP = ((PTD - CTD) * 10000) / (CTO - PTO)
            # print(f"CRP Calculation: (({PTD - CTD}) * 10000) / ({CTO - PTO}) = {CRP}")
        else:
            CRP = 0
            # print(f"CRP SET TO 0 - Conditions not met: CTO > PTO ({CTO} > {PTO}) = {CTO > PTO}, PTD > CTD ({PTD} > {CTD}) = {PTD > CTD}")

        # Calculate all other metrics
        # print("=== DEBUG CALCULATIONS ===")
        
        # Remaining Traveling Distance
        if CRP > 0:
            RTD = ((CTD - DTD) / CRP) * 10000
            # print(f"RTD: (({CTD} - {DTD}) / {CRP}) * 10000 = {RTD}")
        else:
            RTD = 0
            # print(f"RTD SET TO 0 - CRP is 0")

        # Cost per mm Tread Depth
        if (ITD - DTD) > 0:
            Cmm = TPP / (ITD - DTD)
            # print(f"Cmm: {TPP} / ({ITD} - {DTD}) = {Cmm}")
        else:
            Cmm = 0
            # print(f"Cmm SET TO 0 - (ITD - DTD) <= 0")

        # Cost Per 1,000 Km travel
        CKm = 10 * CRP * Cmm
        # print(f"CKm: 10 * {CRP} * {Cmm} = {CKm}")

        # Fuel Consumption Increase
        FCI = ((ITP - CTP) / 10) * 0.4
        # print(f"FCI: (({ITP} - {CTP}) / 10) * 0.4 = {FCI}")

        # Fuel Loss Caused
        # FLC = FCI * (PTM / 100)
        # print(f"FLC: {FCI} * ({PTM} / 100) = {FLC}")

        # Current Tire Value
        if (ITD - DTD) > 0:
            CTV = ((CTD - DTD) / (ITD - DTD)) * TPP
            # print(f"CTV: (({CTD} - {DTD}) / ({ITD} - {DTD})) * {TPP} = {CTV}")
        else:
            CTV = 0
            # print(f"CTV SET TO 0 - (ITD - DTD) <= 0")

        # Balance Travelling Distance
        if CRP > 0:
            BTD = ((CTD - DTD) / CRP) * 10000
            # print(f"BTD: (({CTD} - {DTD}) / {CRP}) * 10000 = {BTD}")
        else:
            BTD = 0
            # print(f"BTD SET TO 0 - CRP is 0")

        # print("=== END DEBUG ===")

        # Create the tire inspection
        tire_inspection = TireInspection.objects.create(
            tire=tire,
            position=position,
            inspection_odometer=inspection_odometer,
            inspector=inspector,
            tread_depth=tread_depth,
            pressure=CTP,
            wear_id=wear_type,
            consumption_rate=CRP,
            remaining_traveling_distance=RTD,
            cost_per_mm_tread_depth=Cmm,
            cost_per_1000_km_travel=CKm,
            fuel_consumption_increase=FCI,
            # fuel_loss_caused=FLC,
            current_tire_value=CTV,
            balance_traveling_distance=BTD,
        )
        
        messages.success(request, 'Tire inspection created successfully!')
        # return redirect('tire_inspections_list')
        work_order_id = request.POST.get('work_order_id')
        
        # Always redirect back with the vehicle filter and create flag
        if work_order_id:
            return redirect(f'/tire-inspections/?work_order={work_order_id}&create=true')
    return redirect('tire_inspections_list')


def tire_inspections_update(request, id):
    tire_inspection = TireInspection.objects.get(id=id)
    if request.method == 'POST':
        # Get data from the form
        tire_id = request.POST.get('tire')
        position_id = request.POST.get('position')
        inspection_odometer = request.POST.get('inspection_odometer')
        inspector_id = request.POST.get('inspector')
        tread_depth = request.POST.get('tread_depth')
        CTP = float(request.POST.get('pressure'))
        wear_id = request.POST.get('wear_id')

        tire = Tire.objects.get(id=tire_id)
        position = TirePosition.objects.get(id=position_id)
        inspector = Employee.objects.get(id=inspector_id)
        wear_type = TireWearType.objects.get(id=wear_id)
        tire_assignment = TireAssignment.objects.get(tire=tire)

        # Current values from this inspection
        CTD = float(tread_depth)
        CTO = int(inspection_odometer)
        DTD = float(tire.pattern.discarding_tread_depth)
        TPP = float(tire.purchase_cost)
        ITD = float(tire.pattern.initial_tread_depth)
        ITP = float(tire.pattern.ideal_tire_pressure)
        PTM = tire_assignment.end_odometer - tire_assignment.start_odometer

        # Find the most recent previous inspection for this tire (excluding current one)
        previous_inspection = TireInspection.objects.filter(
            tire=tire
        ).exclude(id=id).order_by('-inspection_odometer').first()
        
        if previous_inspection:
            PTD = float(previous_inspection.tread_depth)
            PTO = previous_inspection.inspection_odometer
        else:
            PTD = ITD
            first_assignment = tire.assignments.order_by('assignment_date').first()
            PTO = first_assignment.start_odometer if first_assignment else 0

        # Recalculate all metrics (same logic as create view)
        if CTO > PTO and PTD > CTD:
            CRP = ((PTD - CTD) * 10000) / (CTO - PTO)
        else:
            CRP = 0
        
        if CRP > 0:
            RTD = ((CTD - DTD) / CRP) * 10000
            BTD = ((CTD - DTD) / CRP) * 10000
        else:
            RTD = 0
            BTD = 0
        
        if (ITD - DTD) > 0:
            Cmm = TPP / (ITD - DTD)
            CTV = ((CTD - DTD) / (ITD - DTD)) * TPP
        else:
            Cmm = 0
            CTV = 0
        
        CKm = 10 * CRP * Cmm
        FCI = ((ITP - CTP) / 10) * 0.4
        FLC = FCI * (PTM / 100)

        # Update all fields including calculated ones
        tire_inspection.tire = tire
        tire_inspection.position = position
        tire_inspection.inspection_odometer = inspection_odometer
        tire_inspection.inspector = inspector
        tire_inspection.tread_depth = tread_depth
        tire_inspection.pressure = CTP
        tire_inspection.wear_id = wear_type
        
        # Update calculated fields
        tire_inspection.consumption_rate = CRP
        tire_inspection.remaining_traveling_distance = RTD
        tire_inspection.cost_per_mm_tread_depth = Cmm
        tire_inspection.cost_per_1000_km_travel = CKm
        tire_inspection.fuel_consumption_increase = FCI
        tire_inspection.fuel_loss_caused = FLC
        tire_inspection.current_tire_value = CTV
        tire_inspection.balance_traveling_distance = BTD
        
        tire_inspection.save()
        
        messages.success(request, 'Tire inspection updated successfully!')
        return redirect('tire_inspections_list')
    
    return redirect('tire_inspections_list')




