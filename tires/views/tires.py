from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from ..models import Tire, TirePattern, TireStatus, Supplier
from decimal import Decimal, InvalidOperation

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
       

    # Apply filters only if they exist
    if pattern_filter:
        tires = tires.filter(pattern_id=pattern_filter)  # Keep as pattern_id
    
    if status_filter:
        tires = tires.filter(status_id=status_filter)  # Keep as status_id
    
    if supplier_filter:
        tires = tires.filter(supplier_id=supplier_filter)  # Keep as supplier_id
    
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

