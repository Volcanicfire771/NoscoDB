
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import ServiceType
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


