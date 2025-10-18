from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
# from .models import Vehicle, TireStatus, ServiceType, Supplier, Employee, TirePosition, WorkOrder
from .models import *
from decimal import Decimal, InvalidOperation


# Menu Views
def menu_page(request):
    vehicles = Vehicle.objects.all()
    employees = Employee.objects.all()
    context = {
        'vehicles':vehicles,
        'employees':employees,
    }
    return render(request, 'menu/menu_page.html',context)






# Vehicle Views --------------------------------------------------------------------------------------------------
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    
    # Get filter parameters from request
    status_filter = request.GET.get('status_filter', '')
    type_filter = request.GET.get('type_filter', '')
    year_filter = request.GET.get('year_filter', '')
    
    # Apply filters
    if status_filter:
        vehicles = vehicles.filter(status=status_filter)
    if type_filter:
        vehicles = vehicles.filter(vehicle_type=type_filter)
    if year_filter:
        vehicles = vehicles.filter(year=year_filter)
    
    context = {
        'vehicles': vehicles,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'year_filter': year_filter,
    }
    return render(request, 'vehicles/vehicle_list.html', context)

def vehicle_delete(request, id):
    if request.method == 'POST':
        vehicle = get_object_or_404(Vehicle, id=id)
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
    return redirect('vehicle_list')

def vehicle_create(request):
    if request.method == 'POST':

        # Get data from the form
        license_plate = request.POST.get('license_plate')
        make = request.POST.get('make')
        year = request.POST.get('year')
        vehicle_type = request.POST.get('vehicle_type')
        status = request.POST.get('status')
        tire_configuration = request.POST.get('tire_configuration')
        
        # Validations

        # Validate license plate uniqueness
        if Vehicle.objects.filter(license_plate=license_plate).exists():
            messages.error(request, 'License plate already exists!')
            return redirect('vehicle_list')
        
        # Create the vehicle
        vehicle = Vehicle.objects.create(
            license_plate=license_plate,
            make=make,
            year=year,
            vehicle_type=vehicle_type,
            status=status,
            tire_configuration=tire_configuration
        )
        
        messages.success(request, 'Vehicle created successfully!')
    
    return redirect('vehicle_list')

def vehicle_update(request, id):

    vehicle = Vehicle.objects.get(id=id)
    if request.method == 'POST':

        new_license_plate = request.POST.get('license_plate')
        
        # Validations

        # Validate license plate uniqueness
        if Vehicle.objects.filter(license_plate=new_license_plate).exclude(id=id).exists():
            messages.error(request, 'License plate already exists!')
            return redirect('vehicle_list')
        
        # Update data
        vehicle.license_plate = new_license_plate
        vehicle.make = request.POST.get('make')
        vehicle.year = request.POST.get('year')
        vehicle.vehicle_type = request.POST.get('vehicle_type')
        vehicle.status = request.POST.get('status')
        vehicle.tire_configuration = request.POST.get('tire_configuration')
        
        vehicle.save()
        
        messages.success(request, 'Vehicle updated successfully!')
    
    return redirect('vehicle_list')


# Tire Status Views ------------------------------------------------------------------------------------------------------

def tire_status_list(request):
    tire_statuses = TireStatus.objects.all()
    
    context = {
        'tire_statuses': tire_statuses
    }
    
    return render(request, 'tire_status/tire_status_list.html', context)


def tire_status_delete(request, id):
    if request.method == 'POST':
        status = get_object_or_404(TireStatus, id=id)
        status.delete()
        messages.success(request, 'Tire_Status deleted successfully!')
    return redirect('tire_status_list')

def tire_status_create(request):
    if request.method == 'POST':
        
        status_name = request.POST.get('status_name')  
        description = request.POST.get('description')
        
        # Create the status
        status = TireStatus.objects.create(
            status_name=status_name,  
            description=description,
        )
        
        messages.success(request, 'Tire Status created successfully!')  
        return redirect('tire_status_list')  

def tire_status_update(request, id):
    status = TireStatus.objects.get(id=id)
    if request.method == 'POST':
        new_status_name = request.POST.get('status_name')  
        
        # Update data
        status.status_name = new_status_name  
        status.description = request.POST.get('description')
        status.save()
        
        messages.success(request, 'Status updated successfully!')  
        return redirect('tire_status_list')

# Work Orders Views ------------------------------------------------------------------------------------------------------

def work_order_list(request):
    work_orders = WorkOrder.objects.all()
    employees = Employee.objects.all()
    vehicles = Vehicle.objects.all()
    context = {
        'work_orders': work_orders,
        'employees': employees,
        'vehicles': vehicles
    }
    
    return render(request, 'work_orders/work_order_list.html', context)

def work_order_delete(request, id):
    if request.method == 'POST':
        work_order = get_object_or_404(WorkOrder, id=id)
        work_order.delete()
        messages.success(request, 'Work Order deleted successfully!')
    return redirect('work_order_list')

def work_order_create(request):
    if request.method == 'POST':

        # Get data from the form
        work_order_number = request.POST.get('work_order_number')
        date_created = request.POST.get('date_created')
        assigned_to_id = request.POST.get('assigned_to')
        vehicle_id = request.POST.get('vehicle')
        current_mileage = request.POST.get('current_mileage')
        shift_type = request.POST.get('shift_type')
        status = request.POST.get('status')
        cost = request.POST.get('cost')
        
        assigned_to = Employee.objects.get(id=assigned_to_id)
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Validations

        # Validate work order number uniqueness
        if WorkOrder.objects.filter(work_order_number=work_order_number).exists():
            messages.error(request, 'Work order number already exists!')
            return redirect('work_order_list')
        
        # Create the work order
        work_order = WorkOrder.objects.create(
            work_order_number=work_order_number,
            assigned_to=assigned_to,
            vehicle=vehicle,
            current_mileage=current_mileage,
            shift_type=shift_type,
            status=status,
            cost=cost
        )
        
        messages.success(request, 'Work Order created successfully!')
    
    return redirect('tires_list')

def work_order_update(request, id):

    work_order = WorkOrder.objects.get(id=id)
    if request.method == 'POST':

        new_work_order_number = request.POST.get('work_order_number')
        assigned_to_id = request.POST.get('assigned_to')
        vehicle_id = request.POST.get('vehicle')
        
        assigned_to = Employee.objects.get(id=assigned_to_id)
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Validations

        # Validate work order number uniqueness
        if WorkOrder.objects.filter(work_order_number=new_work_order_number).exclude(id=id).exists():
            messages.error(request, 'Work order number already exists!')
            return redirect('work_order_list')
        
        # Update data
        work_order.work_order_number = new_work_order_number
        work_order.assigned_to = assigned_to
        work_order.vehicle = vehicle
        work_order.current_mileage = request.POST.get('current_mileage')
        work_order.shift_type = request.POST.get('shift_type')
        work_order.status = request.POST.get('status')
        work_order.cost = request.POST.get('cost')
        
        work_order.save()
        
        messages.success(request, 'Work Order updated successfully!')
    
    return redirect('work_order_list')


# Service Type Views ------------------------------------------------------------------------------------------------------

def service_type_list(request):
    service_types = ServiceType.objects.all()
    
    context = {
        'service_types': service_types
    }
    
    return render(request, 'service_type/service_type_list.html', context)


def service_type_delete(request, id):
    if request.method == 'POST':
        service = get_object_or_404(ServiceType, id=id)
        service.delete()
        messages.success(request, 'Service Type deleted successfully!')
    return redirect('service_type_list')

def service_type_create(request):
    if request.method == 'POST':
        
        service_name = request.POST.get('service_name')  
        description = request.POST.get('description')
        
        service = ServiceType.objects.create(
            service_name=service_name,  
            description=description,
        )
        
        messages.success(request, 'Service Type created successfully!')  
        return redirect('service_type_list')  

def service_type_update(request, id):
    service = ServiceType.objects.get(id=id)
    if request.method == 'POST':
        new_service_name = request.POST.get('service_name')  
        
        # Update data
        service.service_name = new_service_name  
        service.description = request.POST.get('description')
        service.save()
        
        messages.success(request, 'Service updated successfully!')  
        return redirect('service_type_list')


# Supplier Views ------------------------------------------------------------------------------------------------------

def supplier_list(request):
    suppliers = Supplier.objects.all()
    
    context = {
        'suppliers': suppliers
    }
    return render(request, 'suppliers/supplier_list.html', context)

def supplier_delete(request, id):
    if request.method == 'POST':
        supplier = get_object_or_404(Supplier, id=id)
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
    return redirect('supplier_list')

def supplier_create(request):
    if request.method == 'POST':

        # Get data from the form
        supplier_name = request.POST.get('supplier_name')
        contact_person = request.POST.get('contact_person')
        phone = request.POST.get('phone')
        position = request.POST.get('position')
        email = request.POST.get('email')
        address = request.POST.get('address')
        evaluation = request.POST.get('evaluation')


        
        # Create the supplier
        supplier = Supplier.objects.create(
            supplier_name=supplier_name,
            contact_person=contact_person,
            phone=phone,
            position=position,
            email=email,
            address=address,
            evaluation=evaluation,
        )
        
        messages.success(request, 'Supplier created successfully!')
    
    return redirect('supplier_list')

def supplier_update(request, id):

    supplier = Supplier.objects.get(id=id)
    if request.method == 'POST':

        new_supplier_name = request.POST.get('supplier_name')

        # Update data
        supplier.supplier_name = new_supplier_name
        supplier.contact_person = request.POST.get('contact_person')
        supplier.phone = request.POST.get('phone')
        supplier.position = request.POST.get('position')
        supplier.email = request.POST.get('email')
        supplier.address = request.POST.get('address')
        supplier.evaluation = request.POST.get('evaluation')
        supplier.save()
        
        messages.success(request, 'Supplier updated successfully!')
    
    return redirect('supplier_list')


# Employee Views ------------------------------------------------------------------------------------------------------

def employee_list(request):
    employees = Employee.objects.all()
    
    context = {
        'employees': employees
    }
    # # Get filter parameters from request
    # status_filter = request.GET.get('status_filter', '')
    # type_filter = request.GET.get('type_filter', '')
    # year_filter = request.GET.get('year_filter', '')
    
    # # Apply filters
    # if status_filter:
    #     employees = employees.filter(status=status_filter)
    # if type_filter:
    #     employees = employees.filter(employee_type=type_filter)
    # if year_filter:
    #     employees = employees.filter(year=year_filter)
    
    # context = {
    #     'employees': employees,
    #     'status_filter': status_filter,
    #     'type_filter': type_filter,
    #     'year_filter': year_filter,
    # }
    return render(request, 'employees/employee_list.html', context)

def employee_delete(request, id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=id)
        employee.delete()
        messages.success(request, 'employee deleted successfully!')
    return redirect('employee_list')

def employee_create(request):
    if request.method == 'POST':

        # Get data from the form
        employment_code = request.POST.get('employment_code')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        position = request.POST.get('position')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')

        
        # Validations

        # Validate license plate uniqueness
        if Employee.objects.filter(employment_code=employment_code).exists():
            messages.error(request, 'employee already exists!')
            return redirect('employee_list')
        
        # Create the employee
        employee = Employee.objects.create(
            employment_code=employment_code,
            first_name=first_name,
            last_name=last_name,
            position=position,
            email=email,
            contact_number=contact_number,
        )
        
        messages.success(request, 'Employee created successfully!')
    
    return redirect('employee_list')

def employee_update(request, id):

    employee = Employee.objects.get(id=id)
    if request.method == 'POST':

        new_employment_code = request.POST.get('employment_code')
        
        # Validations

        # Validate license plate uniqueness
        if Employee.objects.filter(employment_code=new_employment_code).exclude(id=id).exists():
            messages.error(request, 'employee code already exists!')
            return redirect('employee_list')
        
        # Update data
        employee.employment_code = new_employment_code
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.position = request.POST.get('position')
        employee.email = request.POST.get('email')
        employee.contact_number = request.POST.get('contact_number')
        
        employee.save()
        
        messages.success(request, 'Employee updated successfully!')
    
    return redirect('employee_list')


# Tire Position Views ------------------------------------------------------------------------------------------------------

def tire_position_list(request):
    tire_positions = TirePosition.objects.all()
    vehicles = Vehicle.objects.all()
    
    # Get filter parameter from request
    vehicle_filter = request.GET.get('vehicle_filter', '')
    
    # Apply filter
    if vehicle_filter:
        tire_positions = tire_positions.filter(vehicle_id=vehicle_filter)
    
    context = {
        'tire_positions': tire_positions,
        'vehicles': vehicles,
        'vehicle_filter': vehicle_filter,
    }
    return render(request, 'tire_positions/tire_position_list.html', context)

def tire_position_delete(request, id):
    if request.method == 'POST':
        tire_position = get_object_or_404(tire_position, id=id)
        tire_position.delete()
        messages.success(request, 'tire_position deleted successfully!')
    return redirect('tire_position_list')

def tire_position_create(request):
    if request.method == 'POST':

        # Get data from the form
        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        position_name = request.POST.get('position_name')
        axle_number = request.POST.get('axle_number')
        wheel_number = request.POST.get('wheel_number')
        is_spare = request.POST.get('is_spare') == 'on'

        
        # Validations

      
        
        # Create the tire_position
        tire_position = TirePosition.objects.create(
            vehicle=vehicle,
            position_name=position_name,
            axle_number=axle_number,
            wheel_number=wheel_number,
            is_spare=is_spare,
        )
        
        messages.success(request, 'tire_position created successfully!')
    
    return redirect('tire_position_list')


def tire_position_update(request, id):
    tire_position = TirePosition.objects.get(id=id)
    if request.method == 'POST':
        # Get the vehicle ID and find the actual Vehicle object
        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Convert checkbox value to boolean
        is_spare = request.POST.get('is_spare') == 'on'
        
        # Update data
        tire_position.vehicle = vehicle
        tire_position.position_name = request.POST.get('position_name')
        tire_position.axle_number = request.POST.get('axle_number')
        tire_position.wheel_number = request.POST.get('wheel_number')
        tire_position.is_spare = is_spare
        
        tire_position.save()
        
        messages.success(request, 'Tire position updated successfully!')
    
    return redirect('tire_position_list')



# Maintenance Records Views ------------------------------------------------------------------------------------------------------

def maintenance_records_list(request):
    # Start with all records
    maintenance_records = MaintenanceRecord.objects.all()
    vehicles = Vehicle.objects.all()
    service_types = ServiceType.objects.all()
    suppliers = Supplier.objects.all()
    
    # Get filter parameters from request
    vehicle_filter = request.GET.get('vehicle_filter', '')
    service_type_filter = request.GET.get('service_type_filter', '')
    service_provider_filter = request.GET.get('service_provider_filter', '')  # Fixed parameter name
    
    # Apply filters only if they exist
    if vehicle_filter:
        maintenance_records = maintenance_records.filter(vehicle_id=vehicle_filter)
    
    if service_type_filter:
        maintenance_records = maintenance_records.filter(service_type_id=service_type_filter)
    
    if service_provider_filter:
        maintenance_records = maintenance_records.filter(service_provider_id=service_provider_filter)
    
    context = {
        'maintenance_records': maintenance_records,
        'vehicles': vehicles,
        'service_types': service_types,
        'suppliers': suppliers,
        'vehicle_filter': vehicle_filter,
        'service_type_filter': service_type_filter,
        'service_provider_filter': service_provider_filter,
    }
    return render(request, 'maintenance_records/maintenance_records_list.html', context)

def maintenance_records_delete(request, id):
    if request.method == 'POST':
        maintenance_record = get_object_or_404(MaintenanceRecord, id=id)
        maintenance_record.delete()
        messages.success(request, 'Maintenance Records deleted successfully!')
    return redirect('maintenance_records_list')

def maintenance_records_create(request):
    if request.method == 'POST':

        # Get data from the form
        vehicle_id = request.POST.get('vehicle')
        service_type_id = request.POST.get('service_type')
        service_date = request.POST.get('service_date')
        service_mileage = request.POST.get('service_mileage')
        cost = request.POST.get('cost')
        service_provider_id = request.POST.get('service_provider')
        notes = request.POST.get('notes')

        vehicle = Vehicle.objects.get(id=vehicle_id)
        service_type = ServiceType.objects.get(id=service_type_id)
        service_provider = Supplier.objects.get(id=service_provider_id)
        # Validations
        
        # Create the maintenance record
        maintenance_record = MaintenanceRecord.objects.create(
            vehicle=vehicle,
            service_type=service_type,
            service_date=service_date,
            service_mileage=service_mileage,
            cost=cost,
            service_provider=service_provider,
            notes=notes,
        )
        
        messages.success(request, 'Maintenance Record created successfully!')
    
    return redirect('maintenance_records_list')

def maintenance_records_update(request, id):

    maintenance_record = MaintenanceRecord.objects.get(id=id)
    if request.method == 'POST':
        
        vehicle_id = request.POST.get('vehicle')
        service_type_id = request.POST.get('service_type')
        service_provider_id = request.POST.get('service_provider')

        vehicle = Vehicle.objects.get(id=vehicle_id)
        service_type = ServiceType.objects.get(id=service_type_id)
        service_provider = Supplier.objects.get(id=service_provider_id)
        
        # Validations

        
        
        # Update data
        maintenance_record.vehicle = vehicle
        maintenance_record.service_type = service_type
        maintenance_record.service_date = request.POST.get('service_date')
        maintenance_record.service_mileage = request.POST.get('service_mileage')
        maintenance_record.cost = request.POST.get('cost')
        maintenance_record.service_provider = service_provider
        maintenance_record.notes = request.POST.get('notes')
        
        maintenance_record.save()
        
        messages.success(request, 'Maintenance Record updated successfully!')
    
    return redirect('maintenance_records_list')


# Tire Inspections Views ------------------------------------------------------------------------------------------------------

def tire_inspections_list(request):
    # Start with all records
    tire_inspections = TireInspection.objects.all()
    tires = Tire.objects.all()
    tire_positions = TirePosition.objects.all()
    employees = Employee.objects.all()
    wear_types = TireWearType.objects.all()

    # Get filter parameters from request
    tire_filter = request.GET.get('tire_filter', '')
    axle_type_filter = request.GET.get('axle_type_filter', '')
    inspector_filter = request.GET.get('inspector_filter', '')
    wear_filter = request.GET.get('wear_filter', '')
    
    # Apply filters only if they exist
    if tire_filter:
        tire_inspections = tire_inspections.filter(tire_id=tire_filter)
    if axle_type_filter:
        tire_inspections = tire_inspections.filter(position__axle_type=axle_type_filter)  
    if inspector_filter:
        tire_inspections = tire_inspections.filter(inspector_id=inspector_filter)
    if wear_filter:
        tire_inspections = tire_inspections.filter(wear_id=wear_filter)  
    
    context = {
        'tire_inspections': tire_inspections,
        'tires': tires,
        'tire_positions': tire_positions,
        'employees': employees,
        'wear_types': wear_types,
        'tire_filter': tire_filter,
        'axle_type_filter': axle_type_filter, 
        'inspector_filter': inspector_filter,
        'wear_filter': wear_filter,  
    }
    return render(request, 'tire_inspections/tire_inspections_list.html', context)

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
        return redirect('tire_inspections_list')
    
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




# Tires Views ------------------------------------------------------------------------------------------------

def tires_list(request):
    # Start with all records
    tires = Tire.objects.all()
    tire_patterns = TirePattern.objects.all()
    tire_statuses = TireStatus.objects.all()
    suppliers = Supplier.objects.all()
    
    # Get filter parameters from request
    pattern_filter = request.GET.get('pattern_filter', '')
    status_filter = request.GET.get('status_filter', '')
    supplier_filter = request.GET.get('supplier_filter', '')
    vehicle_filter = request.GET.get('supplier_filter', '')

    # Apply filters only if they exist
    if pattern_filter:
        tires = tires.filter(pattern_id=pattern_filter)  # Keep as pattern_id
    
    if status_filter:
        tires = tires.filter(status_id=status_filter)  # Keep as status_id
    
    if supplier_filter:
        tires = tires.filter(supplier_id=supplier_filter)  # Keep as supplier_id
    
    if vehicle_filter:
        position = TirePosition.objects.get(vehicle="the one sent from previous link")
    context = {
        'tires': tires,
        'tire_patterns': tire_patterns,
        'tire_statuses': tire_statuses,
        'suppliers': suppliers,
        'pattern_filter': pattern_filter,
        'status_filter': status_filter,
        'supplier_filter': supplier_filter,
    }
    return render(request, 'tires/tires_list.html', context)

def tires_delete(request, id):
    if request.method == 'POST':
        tire = Tire.objects.get(id=id)
        tire.delete()
        messages.success(request, 'Tire deleted successfully!')
    return redirect('tires_list')


def tires_create(request):
    if request.method == 'POST':
        try:
            # Get data from the form
            serial_number = request.POST.get('serial_number')
            pattern_id = request.POST.get('pattern')
            status_id = request.POST.get('status')
            purchase_date = request.POST.get('purchase_date')
            purchase_cost = request.POST.get('purchase_cost')
            supplier_id = request.POST.get('supplier')
            initial_tread_depth = request.POST.get('initial_tread_depth')
            notes = request.POST.get('notes')

            pattern = TirePattern.objects.get(id=pattern_id)
            status = TireStatus.objects.get(id=status_id)
            supplier = Supplier.objects.get(id=supplier_id) if supplier_id else None
            
            # FIX: Convert to Decimal properly
            try:
                purchase_cost_decimal = Decimal(purchase_cost) if purchase_cost else Decimal('0.00')
            except (InvalidOperation, TypeError, ValueError):
                purchase_cost_decimal = Decimal('0.00')
                
            try:
                initial_tread_depth_decimal = Decimal(initial_tread_depth) if initial_tread_depth else Decimal('0.00')
            except (InvalidOperation, TypeError, ValueError):
                initial_tread_depth_decimal = Decimal('0.00')
        
            # Create the tire
            tire = Tire.objects.create(
                serial_number=serial_number,
                pattern=pattern,
                status=status,
                purchase_date=purchase_date,
                purchase_cost=purchase_cost_decimal,  # Use converted Decimal
                supplier=supplier,
                initial_tread_depth=initial_tread_depth_decimal,  # Use converted Decimal
                notes=notes,
            )
            
            messages.success(request, 'Tire created successfully!')
            
        except Exception as e:
            messages.error(request, f'Error creating tire: {str(e)}')
    
    return redirect('tires_list')

def tires_update(request, id):
    tire = Tire.objects.get(id=id)
    if request.method == 'POST':
        try:
            pattern_id = request.POST.get('pattern')
            status_id = request.POST.get('status')
            supplier_id = request.POST.get('supplier')

            pattern = TirePattern.objects.get(id=pattern_id)
            status = TireStatus.objects.get(id=status_id)
            supplier = Supplier.objects.get(id=supplier_id) if supplier_id else None
            
            # FIX: Convert to Decimal properly
            try:
                purchase_cost_decimal = Decimal(request.POST.get('purchase_cost')) if request.POST.get('purchase_cost') else Decimal('0.00')
            except (InvalidOperation, TypeError, ValueError):
                purchase_cost_decimal = Decimal('0.00')
                
            try:
                initial_tread_depth_decimal = Decimal(request.POST.get('initial_tread_depth')) if request.POST.get('initial_tread_depth') else Decimal('0.00')
            except (InvalidOperation, TypeError, ValueError):
                initial_tread_depth_decimal = Decimal('0.00')
            
            # Update data
            tire.serial_number = request.POST.get('serial_number')
            tire.pattern = pattern
            tire.status = status
            tire.purchase_date = request.POST.get('purchase_date')
            tire.purchase_cost = purchase_cost_decimal  # Use converted Decimal
            tire.supplier = supplier
            tire.initial_tread_depth = initial_tread_depth_decimal  # Use converted Decimal
            tire.notes = request.POST.get('notes')
            
            tire.save()
            
            messages.success(request, 'Tire updated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error updating tire: {str(e)}')
    
    return redirect('tires_list')

# Tire Patterns Views ------------------------------------------------------------------------------------------------

def tire_patterns_list(request):
    # Start with all records
    tire_patterns = TirePattern.objects.all()
    
    # Get filter parameters from request
    brand_filter = request.GET.get('brand_filter', '')
    country_filter = request.GET.get('country_filter', '')
    road_type_filter = request.GET.get('road_type_filter', '')
    
    # Apply filters only if they exist
    if brand_filter:
        tire_patterns = tire_patterns.filter(brand_name__icontains=brand_filter)
    if country_filter:
        tire_patterns = tire_patterns.filter(country_of_origin__icontains=country_filter)
    if road_type_filter:
        tire_patterns = tire_patterns.filter(road_type__icontains=road_type_filter)
    
    context = {
        'tire_patterns': tire_patterns,
        'brand_filter': brand_filter,
        'country_filter': country_filter,
        'road_type_filter': road_type_filter,
    }
    return render(request, 'tire_patterns/tire_patterns_list.html', context)

def tire_patterns_delete(request, id):
    if request.method == 'POST':
        tire_pattern = TirePattern.objects.get(id=id)
        tire_pattern.delete()
        messages.success(request, 'Tire pattern deleted successfully!')
    return redirect('tire_patterns_list')

def tire_patterns_create(request):
    if request.method == 'POST':
        # Get data from the form
        pattern_code = request.POST.get('pattern_code')
        brand_name = request.POST.get('brand_name')
        country_of_origin = request.POST.get('country_of_origin')
        load_index = request.POST.get('load_index')
        speed_symbol = request.POST.get('speed_symbol')
        road_type = request.POST.get('road_type')
        
        # Create the tire pattern
        tire_pattern = TirePattern.objects.create(
            pattern_code=pattern_code,
            brand_name=brand_name,
            country_of_origin=country_of_origin,
            load_index=load_index,
            speed_symbol=speed_symbol,
            road_type=road_type,
        )
        
        messages.success(request, 'Tire pattern created successfully!')
    
    return redirect('tire_patterns_list')

def tire_patterns_update(request, id):
    tire_pattern = TirePattern.objects.get(id=id)
    if request.method == 'POST':
        # Update data
        tire_pattern.pattern_code = request.POST.get('pattern_code')
        tire_pattern.brand_name = request.POST.get('brand_name')
        tire_pattern.country_of_origin = request.POST.get('country_of_origin')
        tire_pattern.load_index = request.POST.get('load_index')
        tire_pattern.speed_symbol = request.POST.get('speed_symbol')
        tire_pattern.road_type = request.POST.get('road_type')
        
        tire_pattern.save()
        
        messages.success(request, 'Tire pattern updated successfully!')
    
    return redirect('tire_patterns_list')


# Tire Assignment Views ------------------------------------------------------------------------------------------------------
def tire_assignment_list(request):
    tire_assignments = TireAssignment.objects.all()
    tires = Tire.objects.all()
    tire_positions = TirePosition.objects.all()
    work_orders = WorkOrder.objects.all()
    tire_inspections = TireInspection.objects.all()

    context = {
        'tire_assignments': tire_assignments,
        'tires': tires,
        'tire_positions': tire_positions,
        'work_orders': work_orders,
        'tire_inspections': tire_inspections,
    }
    return render(request, 'tire_assignments/tire_assignment_list.html', context)

def tire_assignment_delete(request, id):
    tire_assignment = get_object_or_404(TireAssignment, id=id)
    if request.method == 'POST':
        tire_assignment.delete()
        messages.success(request, 'Tire assignment deleted successfully!')
    return redirect('tire_assignment_list')

def tire_assignment_create(request):
    if request.method == 'POST':
        # Get data from the form
        tire_id = request.POST.get('tire')
        tire_position_from_id = request.POST.get('tire_position_from')
        tire_position_to_id = request.POST.get('tire_position_to')
        work_order_id = request.POST.get('work_order')
        tire_inspection_id = request.POST.get('tire_inspection')
        assignment_date = request.POST.get('assignment_date')
        removal_date = request.POST.get('removal_date')
        start_odometer = request.POST.get('start_odometer')
        end_odometer = request.POST.get('end_odometer')
        removal_mileage = request.POST.get('removal_mileage')
        reason_for_removal = request.POST.get('reason_for_removal')

        tire_inspection = TireInspection.objects.get(id=tire_inspection_id)


        tire = get_object_or_404(Tire, id=tire_id)
        tire_position_from = get_object_or_404(TirePosition, id=tire_position_from_id)
        tire_position_to = get_object_or_404(TirePosition, id=tire_position_to_id)
        work_order = get_object_or_404(WorkOrder, id=work_order_id)
        tire_inspection = get_object_or_404(TireInspection, id=tire_inspection_id)
        

        # Create the tire assignment
        tire_assignment = TireAssignment.objects.create(
            tire=tire,
            tire_position_from=tire_position_from,
            tire_position_to=tire_position_to,
            assignment_date=assignment_date,
            removal_date=removal_date,
            start_odometer=start_odometer,
            end_odometer=end_odometer,
            work_order=work_order,
            tire_inspection=tire_inspection,
            removal_mileage=removal_mileage,
            reason_for_removal=reason_for_removal,
        )
        
        messages.success(request, 'Tire assignment created successfully!')
    return redirect('tire_assignment_list')
    
def tire_assignment_update(request, id):
    tire_assignment = get_object_or_404(TireAssignment, id=id)
    if request.method == 'POST':

        # Get data from the form
        tire_id = request.POST.get('tire')
        tire_position_from_id = request.POST.get('tire_position_from')
        tire_position_to_id = request.POST.get('tire_position_to')
        work_order_id = request.POST.get('work_order')
        tire_inspection_id = request.POST.get('tire_inspection')
        assignment_date = request.POST.get('assignment_date')
        removal_date = request.POST.get('removal_date')
        start_odometer = request.POST.get('start_odometer')
        end_odometer = request.POST.get('end_odometer')
        removal_mileage = request.POST.get('removal_mileage')
        reason_for_removal = request.POST.get('reason_for_removal')

        tire = Tire.objects.get(id=tire_id)
        tire_position_from = TirePosition.objects.get(id=tire_position_from_id)
        tire_position_to = TirePosition.objects.get(id=tire_position_to_id)
        work_order = WorkOrder.objects.get(id=work_order_id)
        tire_inspection = TireInspection.objects.get(id=tire_inspection_id)

        # Update the tire assignment
        tire_assignment.tire = tire
        tire_assignment.tire_position_from = tire_position_from
        tire_assignment.tire_position_to = tire_position_to
        tire_assignment.assignment_date = assignment_date
        tire_assignment.removal_date = removal_date
        tire_assignment.start_odometer = start_odometer
        tire_assignment.end_odometer = end_odometer
        tire_assignment.work_order = work_order
        tire_assignment.tire_inspection = tire_inspection
        tire_assignment.removal_mileage = removal_mileage
        tire_assignment.reason_for_removal = reason_for_removal
        tire_assignment.save()

        messages.success(request, 'Tire assignment updated successfully!')
    return redirect('tire_assignment_list')
