from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from ..models import Tire, TirePattern, TireStatus, Supplier, TirePosition
from decimal import Decimal, InvalidOperation

# Tires Views ------------------------------------------------------------------------------------------------

def tires_list(request):
    # Start with all records
    tires = Tire.objects.all()
    tire_patterns = TirePattern.objects.all()
    tire_statuses = TireStatus.objects.all()
    tire_positions = TirePosition.objects.all()
    suppliers = Supplier.objects.all()

    active_count = Tire.objects.filter(
        Q(status=1) | Q(status=6) | Q(status=7)
    ).count()
    under_repair_count = Tire.objects.filter(status=3).count()
    inactive_count = Tire.objects.filter(
        Q(status=2) | Q(status=4)
    ).count()

    context = {
        'tires': tires,
        'tire_patterns': tire_patterns,
        'tire_statuses': tire_statuses,
        'tire_positions': tire_positions,
        'suppliers': suppliers,
        'active_count': active_count,
        'under_repair_count': under_repair_count,
        'inactive_count': inactive_count,
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
            size = request.POST.get('size')
            status_id = request.POST.get('status')
            purchase_date = request.POST.get('purchase_date')
            purchase_cost = request.POST.get('purchase_cost')
            supplier_id = request.POST.get('supplier')
            initial_tread_depth = request.POST.get('initial_tread_depth')
            last_tread_depth = request.POST.get('last_tread_depth')
            retread_count = request.POST.get('retread_count')
            maximum_retreads = request.POST.get('maximum_retreads')
            current_position_id = request.POST.get('current_position')
            tire_mileage = request.POST.get('tire_mileage')
            notes = request.POST.get('notes')
        

            pattern = TirePattern.objects.get(id=pattern_id)
            status = TireStatus.objects.get(id=status_id)
            supplier = Supplier.objects.get(id=supplier_id) if supplier_id else None
            current_position = TirePosition.objects.get(id=current_position_id) if current_position_id else None
            # FIX: Convert to Decimal properly
            try:
                purchase_cost_decimal = Decimal(purchase_cost) if purchase_cost else Decimal('0.00')
            except (InvalidOperation, TypeError, ValueError):
                purchase_cost_decimal = Decimal('0.00')
                
            try:
                initial_tread_depth_decimal = Decimal(initial_tread_depth) if initial_tread_depth else Decimal('0.00')
            except (InvalidOperation, TypeError, ValueError):
                initial_tread_depth_decimal = Decimal('0.00')

            try:
                last_tread_depth_decimal = Decimal(last_tread_depth) if last_tread_depth else Decimal('0.00')
            except (InvalidOperation, TypeError, ValueError):
                last_tread_depth_decimal = Decimal('0.00')

            # Create the tire
            tire = Tire.objects.create(
                serial_number=serial_number,
                pattern=pattern,
                size=size,
                status=status,
                purchase_date=purchase_date,
                purchase_cost=purchase_cost_decimal,  # Use converted Decimal
                supplier=supplier,
                initial_tread_depth=initial_tread_depth_decimal,  # Use converted Decimal
                last_tread_depth=last_tread_depth_decimal,  # Use converted Decimal
                retread_count=retread_count,
                maximum_retreads=maximum_retreads,
                current_position=current_position,
                tire_mileage=tire_mileage,
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
            current_position_id = request.POST.get('current_position')  


            pattern = TirePattern.objects.get(id=pattern_id)
            status = TireStatus.objects.get(id=status_id)
            supplier = Supplier.objects.get(id=supplier_id) if supplier_id else None
            current_position = TirePosition.objects.get(id=current_position_id) if current_position_id else None


            # FIX: Convert to Decimal properly
            try:
                purchase_cost_decimal = Decimal(request.POST.get('purchase_cost')) if request.POST.get('purchase_cost') else Decimal('0.00')
            except (InvalidOperation, TypeError, ValueError):
                purchase_cost_decimal = Decimal('0.00')
                
            try:
                initial_tread_depth_decimal = Decimal(request.POST.get('initial_tread_depth')) if request.POST.get('initial_tread_depth') else Decimal('0.00')
            except (InvalidOperation, TypeError, ValueError):
                initial_tread_depth_decimal = Decimal('0.00')
            
            try:
                last_tread_depth_decimal = Decimal(request.POST.get('last_tread_depth')) if request.POST.get('last_tread_depth') else Decimal('0.00')
            except (InvalidOperation, TypeError, ValueError):
                last_tread_depth_decimal = Decimal('0.00')

            # Update data
            tire.serial_number = request.POST.get('serial_number')
            tire.pattern = pattern
            tire.size = request.POST.get('size')
            tire.status = status
            tire.purchase_date = request.POST.get('purchase_date')
            tire.purchase_cost = purchase_cost_decimal  # Use converted Decimal
            tire.supplier = supplier
            tire.initial_tread_depth = initial_tread_depth_decimal  # Use converted Decimal
            tire.last_tread_depth = last_tread_depth_decimal  # Use converted Decimal
            tire.retread_count = request.POST.get('retread_count')
            tire.maximum_retreads = request.POST.get('maximum_retreads')
            tire.current_position = current_position
            tire.tire_mileage = request.POST.get('tire_mileage')
            tire.notes = request.POST.get('notes')
            
            tire.save()
            
            messages.success(request, 'Tire updated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error updating tire: {str(e)}')
    
    return redirect('tires_list')

