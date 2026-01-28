from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import TirePosition, Vehicle, Tire

def tire_position_list(request):
    tire_positions = TirePosition.objects.all()
    vehicles = Vehicle.objects.all()
    tires = Tire.objects.all()
    
    vehicle_filter = request.GET.get('vehicle_filter', '')
    
    if vehicle_filter:
        tire_positions = tire_positions.filter(vehicle_id=vehicle_filter)
    
    vehicle_filter = request.GET.get('vehicle_filter', '')
    if vehicle_filter:
        vehicle_positions = TirePosition.objects.filter(vehicle_id=vehicle_filter)
        mounted_tire_ids = vehicle_positions.exclude(
            mounted_tire__isnull=True
        ).values_list('mounted_tire_id', flat=True)
        tires = Tire.objects.filter(id__in=mounted_tire_ids)
    
    context = {
        'tire_positions': tire_positions,
        'vehicles': vehicles,
        'vehicle_filter': vehicle_filter,
        'tires': tires,
    }
    return render(request, 'tire_positions/tire_position_list.html', context)

def tire_position_delete(request, id):
    if request.method == 'POST':
        tire_position = get_object_or_404(TirePosition, id=id)
        tire_position.delete()
        messages.success(request, 'Tire position deleted successfully!')
    return redirect('tire_position_list')

def tire_position_create(request):
    if request.method == 'POST':
        # Get data from the form
        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        position_name = request.POST.get('position_name')
        axle_number = request.POST.get('axle_number')
        wheel_number = request.POST.get('wheel_number')
        axle_type = request.POST.get('axle_type')
        is_spare = request.POST.get('is_spare') == 'on'
        mounted_tire_id = request.POST.get('mounted_tire')
        
        # Handle empty mounted_tire field
        tire = None
        if mounted_tire_id:  # Check if it's not empty
            try:
                tire = Tire.objects.get(id=mounted_tire_id)
            except Tire.DoesNotExist:
                messages.error(request, 'Selected tire does not exist')
                return redirect('tire_position_list')
        
        # Create the tire_position
        tire_position = TirePosition.objects.create(
            vehicle=vehicle,
            position_name=position_name,
            axle_number=axle_number,
            wheel_number=wheel_number,
            axle_type=axle_type,
            is_spare=is_spare,
            mounted_tire=tire  # This can be None
        )
        
        messages.success(request, 'Tire position created successfully!')
    
    return redirect('tire_position_list')

def tire_position_update(request, id):
    tire_position = get_object_or_404(TirePosition, id=id)
    
    if request.method == 'POST':
        # Get the vehicle ID and find the actual Vehicle object
        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Get mounted_tire_id (might be empty string)
        mounted_tire_id = request.POST.get('mounted_tire')
        
        # Handle empty mounted_tire field
        tire = None
        if mounted_tire_id:  # Check if it's not empty
            try:
                tire = Tire.objects.get(id=mounted_tire_id)
            except Tire.DoesNotExist:
                messages.error(request, 'Selected tire does not exist')
                return redirect('tire_position_list')
        
        # Convert checkbox value to boolean
        is_spare = request.POST.get('is_spare') == 'on'
        
        # Update data
        tire_position.vehicle = vehicle
        tire_position.position_name = request.POST.get('position_name')
        tire_position.axle_number = request.POST.get('axle_number')
        tire_position.wheel_number = request.POST.get('wheel_number')
        tire_position.axle_type = request.POST.get('axle_type')
        tire_position.is_spare = is_spare
        tire_position.mounted_tire = tire  # This can be None
        tire_position.save()
        
        messages.success(request, 'Tire position updated successfully!')
    
    return redirect('tire_position_list')