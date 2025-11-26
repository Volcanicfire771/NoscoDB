from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import Supplier, TirePattern
# Tire Patterns Views ------------------------------------------------------------------------------------------------

def tire_patterns_list(request):
    # Start with all records
    tire_patterns = TirePattern.objects.all()
    suppliers = Supplier.objects.all()
    # Get filter parameters from request
    brand_filter = request.GET.get('brand_filter', '')
    country_filter = request.GET.get('country_filter', '')
    road_type_filter = request.GET.get('road_type_filter', '')
    
    # Apply filters only if they exist
    if brand_filter:
        tire_patterns = tire_patterns.filter(brand_name=brand_filter)
    if country_filter:
        tire_patterns = tire_patterns.filter(country_of_origin__icontains=country_filter)
    if road_type_filter:
        tire_patterns = tire_patterns.filter(road_type__icontains=road_type_filter)
    
    context = {
        'tire_patterns': tire_patterns,
        'suppliers': suppliers,
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
        brand_name_id = request.POST.get('brand_name')
        country_of_origin = request.POST.get('country_of_origin')
        load_index = request.POST.get('load_index')
        speed_symbol = request.POST.get('speed_symbol')
        road_type = request.POST.get('road_type')

        brand_name = Supplier.objects.get(id=brand_name_id)
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

        brand_name_id = request.POST.get('brand_name')

        brand_name = Supplier.objects.get(id=brand_name_id)


        # Update data
        tire_pattern.pattern_code = request.POST.get('pattern_code')
        tire_pattern.brand_name = brand_name
        tire_pattern.country_of_origin = request.POST.get('country_of_origin')
        tire_pattern.load_index = request.POST.get('load_index')
        tire_pattern.speed_symbol = request.POST.get('speed_symbol')
        tire_pattern.road_type = request.POST.get('road_type')
        
        tire_pattern.save()
        
        messages.success(request, 'Tire pattern updated successfully!')
    
    return redirect('tire_patterns_list')

