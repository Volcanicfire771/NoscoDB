from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import TirePosition, Vehicle, Tire
# Tire Position Views ------------------------------------------------------------------------------------------------------

def tire_position_list(request):
    tire_positions = TirePosition.objects.all()
    vehicles = Vehicle.objects.all()
    tires = Tire.objects.all()
    
    # Get filter parameter from request
    vehicle_filter = request.GET.get('vehicle_filter', '')
    
    # Apply filter to tire positions
    if vehicle_filter:
        tire_positions = tire_positions.filter(vehicle_id=vehicle_filter)
    
    # Get tires for the selected vehicle (for the dropdown)
    vehicle_filter = request.GET.get('vehicle_filter', '')
    if vehicle_filter:
        # Get all tire positions for this vehicle
        vehicle_positions = TirePosition.objects.filter(vehicle_id=vehicle_filter)
        
        # Get tires that are currently mounted on these positions
        mounted_tire_ids = vehicle_positions.exclude(
            mounted_tire__isnull=True
        ).values_list('mounted_tire_id', flat=True)
        
        # Filter tires to show only those mounted on this vehicle
        tires = Tire.objects.filter(id__in=mounted_tire_ids)
    
    # print("This is the vehicle Filter: " + vehicle_filter)

    context = {
        'tire_positions': tire_positions,
        'vehicles': vehicles,
        'vehicle_filter': vehicle_filter,
        'tires': tires,
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
        mounted_tire = request.POST.get('mounted_tire')
        
        tire = Tire.objects.get(id = mounted_tire)
        # Validations
        print("Tire: " + tire.serial_number)
      
        
        # Create the tire_position
        tire_position = TirePosition.objects.create(
            vehicle=vehicle,
            position_name=position_name,
            axle_number=axle_number,
            wheel_number=wheel_number,
            is_spare=is_spare,
            mounted_tire=tire
        )
        
        messages.success(request, 'tire_position created successfully!')
    
    return redirect('tire_position_list')


def tire_position_update(request, id):
    tire_position = TirePosition.objects.get(id=id)
    if request.method == 'POST':
        # Get the vehicle ID and find the actual Vehicle object
        vehicle_id = request.POST.get('vehicle')
        mounted_tire_id =request.POST.get('mounted_tire')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        tire = Tire.objects.get(id = mounted_tire_id)
        # Convert checkbox value to boolean
        is_spare = request.POST.get('is_spare') == 'on'
        
        # Update data
        tire_position.vehicle = vehicle
        tire_position.position_name = request.POST.get('position_name')
        tire_position.axle_number = request.POST.get('axle_number')
        tire_position.wheel_number = request.POST.get('wheel_number')
        tire_position.is_spare = is_spare
        tire_position.mounted_tire = tire
        tire_position.save()
        
        messages.success(request, 'Tire position updated successfully!')
    
    return redirect('tire_position_list')



