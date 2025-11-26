from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from ..models import Vehicle


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
