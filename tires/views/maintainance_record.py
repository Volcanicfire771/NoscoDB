from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import MaintenanceRecord, Tire, ServiceType, Supplier
# Maintenance Records Views ------------------------------------------------------------------------------------------------------

def maintenance_records_list(request):
    # Start with all records
    maintenance_records = MaintenanceRecord.objects.all()
    tires = Tire.objects.all()
    service_types = ServiceType.objects.all()
    suppliers = Supplier.objects.all()
    
    # Get filter parameters from request
    tire_filter = request.GET.get('tire_filter', '')
    service_type_filter = request.GET.get('service_type_filter', '')
    service_provider_filter = request.GET.get('service_provider_filter', '')  # Fixed parameter name
    
    # Apply filters only if they exist
    if tire_filter:
        maintenance_records = maintenance_records.filter(tire_id=tire_filter)

    if service_type_filter:
        maintenance_records = maintenance_records.filter(service_type_id=service_type_filter)
    
    if service_provider_filter:
        maintenance_records = maintenance_records.filter(service_provider_id=service_provider_filter)
    
    context = {
        'maintenance_records': maintenance_records,
        'tires': tires,
        'service_types': service_types,
        'suppliers': suppliers,
        'tire_filter': tire_filter,
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
        tire_id = request.POST.get('tire')
        service_type_id = request.POST.get('service_type')
        service_date = request.POST.get('service_date')
        service_mileage = request.POST.get('service_mileage')
        cost = request.POST.get('cost')
        service_provider_id = request.POST.get('service_provider')
        notes = request.POST.get('notes')

        tire = Tire.objects.get(id=tire_id)
        service_type = ServiceType.objects.get(id=service_type_id)
        service_provider = Supplier.objects.get(id=service_provider_id)
        # Validations
        
        # Create the maintenance record
        maintenance_record = MaintenanceRecord.objects.create(
            tire=tire,
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
        
        tire_id = request.POST.get('tire')
        service_type_id = request.POST.get('service_type')
        service_provider_id = request.POST.get('service_provider')

        tire = Tire.objects.get(id=tire_id)
        service_type = ServiceType.objects.get(id=service_type_id)
        service_provider = Supplier.objects.get(id=service_provider_id)
        
        # Validations

        
        
        # Update data
        maintenance_record.tire = tire
        maintenance_record.service_type = service_type
        maintenance_record.service_date = request.POST.get('service_date')
        maintenance_record.service_mileage = request.POST.get('service_mileage')
        maintenance_record.cost = request.POST.get('cost')
        maintenance_record.service_provider = service_provider
        maintenance_record.notes = request.POST.get('notes')
        
        maintenance_record.save()
        
        messages.success(request, 'Maintenance Record updated successfully!')
    
    return redirect('maintenance_records_list')

