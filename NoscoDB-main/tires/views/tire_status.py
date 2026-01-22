from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import TireStatus

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
