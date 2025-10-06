from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Vehicle, TireStatus, ServiceType, Supplier, Employee, TirePosition


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
        
        messages.success(request, 'Vehicle created successfully!')
    
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
    # # Get filter parameters from request
    # status_filter = request.GET.get('status_filter', '')
    # type_filter = request.GET.get('type_filter', '')
    # year_filter = request.GET.get('year_filter', '')
    
    # # Apply filters
    # if status_filter:
    #     suppliers = suppliers.filter(status=status_filter)
    # if type_filter:
    #     suppliers = suppliers.filter(supplier_type=type_filter)
    # if year_filter:
    #     suppliers = suppliers.filter(year=year_filter)
    
    # context = {
    #     'suppliers': suppliers,
    #     'status_filter': status_filter,
    #     'type_filter': type_filter,
    #     'year_filter': year_filter,
    # }
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

        
        # Validations

        # Validate license plate uniqueness
        if Supplier.objects.filter(supplier_name=supplier_name).exists():
            messages.error(request, 'Supplier already exists!')
            return redirect('supplier_list')
        
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
        
        # Validations

        # Validate license plate uniqueness
        if Supplier.objects.filter(supplier_name=new_supplier_name).exclude(id=id).exists():
            messages.error(request, 'Supplier name already exists!')
            return redirect('supplier_list')
        
        # Update data
        supplier.supplier_name = new_supplier_name
        supplier.contact_person = request.POST.get('contact_person')
        supplier.phone = request.POST.get('phone')
        supplier.position = request.POST.get('position')
        supplier.email = request.POST.get('email')
        supplier.address = request.POST.get('address')
        supplier.evaluation = request.POST.get('evaluation')
        
        supplier.save()
        
        messages.success(request, 'supplier created successfully!')
    
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
        employee = get_object_or_404(employee, id=id)
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
        
        messages.success(request, 'employee created successfully!')
    
    return redirect('employee_list')

def employee_update(request, id):

    employee = Employee.objects.get(id=id)
    if request.method == 'POST':

        new_employment_code = request.POST.get('employment_code')
        
        # Validations

        # Validate license plate uniqueness
        if Employee.objects.filter(employee_name=new_employment_code).exclude(id=id).exists():
            messages.error(request, 'employee name already exists!')
            return redirect('employee_list')
        
        # Update data
        employee.employment_code = new_employment_code
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.position = request.POST.get('position')
        employee.email = request.POST.get('email')
        employee.contact_number = request.POST.get('contact_number')
        
        employee.save()
        
        messages.success(request, 'Employee created successfully!')
    
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