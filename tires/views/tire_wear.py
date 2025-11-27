from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import TireWearType

# TireWearType Views --------------------------------------------------------------------------------------------------
def tire_wear_type_list(request):
    wearTypes = TireWearType.objects.all()
    
    context = {
        'wearTypes': wearTypes,
    }
    return render(request, 'tire_wear_type/tire_wear_type_list.html', context)

def tire_wear_type_delete(request, id):
    if request.method == 'POST':
        wear_type = get_object_or_404(TireWearType, id=id)
        wear_type.delete()
        messages.success(request, 'Wear Type deleted successfully!')
    return redirect('tire_wear_type_list')

def tire_wear_type_create(request):
    if request.method == 'POST':

        # Get data from the form
        name = request.POST.get('name')
        cause = request.POST.get('wear_common_cause')
        recovery_scheme = request.POST.get('recovery_scheme')
        # Validations

        # Validate license plate uniqueness
        if TireWearType.objects.filter(name=name).exists():
            messages.error(request, 'Wear Type already exists!')
            return redirect('tire_wear_type_list')
        
        # Create the wear type
        wear_type = TireWearType.objects.create(
            name=name,
            wear_common_cause=cause,
            recovery_scheme=recovery_scheme,
        )
        
        messages.success(request, 'Tire Wear created successfully!')
    
    return redirect('tire_wear_type_list')

def tire_wear_type_update(request, id):

    wear_type = TireWearType.objects.get(id=id)
    if request.method == 'POST':

        new_name = request.POST.get('name')
        
        # Validations

        # Validate name uniqueness
        if TireWearType.objects.filter(name=new_name).exclude(id=id).exists():
            messages.error(request, 'Tire Wear Type already exists!')
            return redirect('tire_wear_type_list')
        
        # Update data
        wear_type.name = new_name
        wear_type.wear_common_cause = request.POST.get('wear_common_cause')
        wear_type.recovery_scheme = request.POST.get('recovery_scheme')
        # print(f"{new_name}::::{ request.POST.get('wear_common_cause')}::::{request.POST.get('recovery_scheme')}")


        wear_type.save()
        
        messages.success(request, 'Tire Wear Type updated successfully!')
    
    return redirect('tire_wear_type_list')
