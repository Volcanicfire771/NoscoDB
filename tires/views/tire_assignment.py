from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import TireAssignment, Tire, Vehicle, TirePosition, TireInspection, WorkOrder

# Tire Assignment Views ------------------------------------------------------------------------------------------------------
def tire_assignment_list(request):
    # Get all necessary data
    vehicles = Vehicle.objects.all()
    
    # Positions WITH tires (for "From Position")
    positions_with_tires = TirePosition.objects.filter(
        mounted_tire__isnull=False
    ).select_related('vehicle', 'mounted_tire')
    
    # EMPTY positions (for "To Position")
    empty_positions = TirePosition.objects.filter(
        mounted_tire__isnull=True
    ).select_related('vehicle')
    
    # Open work orders
    open_work_orders = WorkOrder.objects.filter(
        status='OPENED'
    ).select_related('vehicle')
    
    # Tire inspections (for optional field)
    tire_inspections = TireInspection.objects.all().select_related('tire')
    
    # Existing assignments for table
    tire_assignments = TireAssignment.objects.all()
    
    context = {
        'vehicles': vehicles,
        'positions_with_tires': positions_with_tires,
        'empty_positions': empty_positions,
        'open_work_orders': open_work_orders,
        'tire_inspections': tire_inspections,
        'tire_assignments': tire_assignments,
    }
    
    return render(request, 'tire_assignments/tire_assignment_list.html', context)

def tire_assignment_delete(request, id):
    tire_assignment = get_object_or_404(TireAssignment, id=id)
    if request.method == 'POST':
        tire_assignment.delete()
        messages.success(request, 'Tire assignment deleted successfully!')
    return redirect('tire_assignment_list')

def tire_assignment_create(request):
    if request.method == 'POST':
        try:
            # Get all data from form
            tire_id = request.POST.get('tire')
            from_position_id = request.POST.get('tire_position_from')
            to_position_id = request.POST.get('tire_position_to')
            work_order_id = request.POST.get('work_order')
            inspection_id = request.POST.get('inspection')
            assignment_date = request.POST.get('assignment_date')
            removal_date = request.POST.get('removal_date')
            reason_for_removal = request.POST.get('reason_for_removal')
            notes = request.POST.get('notes')
            
            # Get objects (handle optional fields)
            tire = Tire.objects.get(id=tire_id)
            from_position = TirePosition.objects.get(id=from_position_id) if from_position_id else None
            to_position = TirePosition.objects.get(id=to_position_id)
            work_order = WorkOrder.objects.get(id=work_order_id)
            inspection = TireInspection.objects.get(id=inspection_id) if inspection_id else None
            
            # VALIDATION 1: Check tire is in from_position (if from_position provided)
            if from_position and from_position.mounted_tire != tire:
                messages.error(request, 'Selected tire is not in the source position!')
                return redirect('tire_assignment_list')
            
            # VALIDATION 2: Check to_position is empty
            if to_position.mounted_tire is not None:
                messages.error(request, 'Target position is not empty!')
                return redirect('tire_assignment_list')
            
            # VALIDATION 3: If moving between vehicles
            if from_position and from_position.vehicle != to_position.vehicle:
                # Check work order is for from_vehicle
                if work_order.vehicle != from_position.vehicle:
                    messages.error(request, 'Work order must be for the source vehicle!')
                    return redirect('tire_assignment_list')
                
                # Check if to_vehicle has open work orders
                to_vehicle_open_work_orders = WorkOrder.objects.filter(
                    vehicle=to_position.vehicle,
                    status__in=['OPENED', 'OPEN', 'IN_PROGRESS']  # Fixed status name
                ).exists()
                
                if not to_vehicle_open_work_orders:
                    messages.error(request, 'Target vehicle has no open work orders!')
                    return redirect('tire_assignment_list')
            
            # VALIDATION 4: If inspection provided, check it's for the correct tire
            if inspection and inspection.tire != tire:
                messages.error(request, 'Selected inspection is not for this tire!')
                return redirect('tire_assignment_list')
            
            # VALIDATION 5: Check tire can be assigned
            if not tire.can_be_assigned:
                messages.error(request, 'This tire cannot be assigned (may be scrapped or in invalid status)!')
                return redirect('tire_assignment_list')
            
            # Create the tire assignment
            tire_assignment = TireAssignment.objects.create(
                tire=tire,
                tire_position_from=from_position,
                tire_position_to=to_position,
                work_order=work_order,
                inspection=inspection,
                assignment_date=assignment_date,
                removal_date=removal_date if removal_date else None,
                reason_for_removal=reason_for_removal if reason_for_removal else '',
                notes=notes if notes else '',
            )
            
            # UPDATE TIRE POSITIONS
            if from_position:
                from_position.mounted_tire = None
                from_position.save()
            
            to_position.mounted_tire = tire
            to_position.save()
            
            # UPDATE TIRE ITSELF
            tire.current_position = to_position
            tire.current_vehicle = to_position.vehicle
            tire.save()  # Removed last_assignment since it's not in the model
            
            # UPDATE RELATED INSPECTIONS (CRITICAL!)
            if inspection:
                # Update the inspection's position and work order
                inspection.position = to_position
                inspection.work_order = work_order
                inspection.save()
            
            # Also update any other inspections for this tire
            if from_position:  # Only update if there was a from position
                TireInspection.objects.filter(
                    tire=tire,
                    position=from_position
                ).update(position=to_position)
            
            messages.success(request, 'Tire assignment created successfully!')
            
        except Tire.DoesNotExist:
            messages.error(request, 'Selected tire does not exist!')
        except TirePosition.DoesNotExist:
            messages.error(request, 'Selected position does not exist!')
        except WorkOrder.DoesNotExist:
            messages.error(request, 'Selected work order does not exist!')
        except TireInspection.DoesNotExist:
            messages.error(request, 'Selected inspection does not exist!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('tire_assignment_list')

def tire_assignment_update(request, id):
    tire_assignment = get_object_or_404(TireAssignment, id=id)
    
    if request.method == 'POST':
        try:
            # Get OLD values before update
            old_to_position = tire_assignment.tire_position_to
            old_from_position = tire_assignment.tire_position_from
            old_tire = tire_assignment.tire
            
            # Get data from the form
            tire_id = request.POST.get('tire')
            tire_position_from_id = request.POST.get('tire_position_from')
            tire_position_to_id = request.POST.get('tire_position_to')
            work_order_id = request.POST.get('work_order')
            inspection_id = request.POST.get('inspection')  # Changed from tire_inspection to match template
            assignment_date = request.POST.get('assignment_date')
            removal_date = request.POST.get('removal_date')
            reason_for_removal = request.POST.get('reason_for_removal')
            
            # Get objects
            tire = Tire.objects.get(id=tire_id)
            tire_position_from = TirePosition.objects.get(id=tire_position_from_id) if tire_position_from_id else None
            tire_position_to = TirePosition.objects.get(id=tire_position_to_id)
            work_order = WorkOrder.objects.get(id=work_order_id)
            inspection = TireInspection.objects.get(id=inspection_id) if inspection_id else None
            
            # VALIDATIONS
            # Check if positions have changed
            if old_to_position != tire_position_to:
                # Check new to_position is empty
                if tire_position_to.mounted_tire is not None:
                    messages.error(request, 'Target position is not empty!')
                    return redirect('tire_assignment_list')
            
            # Check tire is in from_position (if from_position provided)
            if tire_position_from and tire_position_from.mounted_tire != tire:
                messages.error(request, 'Selected tire is not in the source position!')
                return redirect('tire_assignment_list')
            
            # Check inspection is for correct tire
            if inspection and inspection.tire != tire:
                messages.error(request, 'Selected inspection is not for this tire!')
                return redirect('tire_assignment_list')
            
            # Update assignment
            tire_assignment.tire = tire
            tire_assignment.tire_position_from = tire_position_from
            tire_assignment.tire_position_to = tire_position_to
            tire_assignment.assignment_date = assignment_date
            tire_assignment.removal_date = removal_date if removal_date else None
            tire_assignment.work_order = work_order
            tire_assignment.inspection = inspection
            tire_assignment.reason_for_removal = reason_for_removal if reason_for_removal else ''
            tire_assignment.save()
            
            # UPDATE POSITIONS IF CHANGED
            if old_to_position != tire_position_to:
                # Remove tire from old position
                if old_to_position and old_to_position.mounted_tire == old_tire:
                    old_to_position.mounted_tire = None
                    old_to_position.save()
                
                # Mount tire in new position
                tire_position_to.mounted_tire = tire
                tire_position_to.save()
                
                # Update old from position if it exists
                if old_from_position and old_from_position != tire_position_from:
                    # If old_from_position was different, update it
                    old_from_position.mounted_tire = None
                    old_from_position.save()
            
            # Update tire's current position
            tire.current_position = tire_position_to
            tire.current_vehicle = tire_position_to.vehicle
            tire.save()
            
            # Update inspections
            if inspection:
                inspection.position = tire_position_to
                inspection.work_order = work_order
                inspection.save()
            
            # Update any other inspections for this tire at old position
            if old_to_position and old_to_position != tire_position_to:
                TireInspection.objects.filter(
                    tire=tire,
                    position=old_to_position
                ).update(position=tire_position_to)
            
            messages.success(request, 'Tire assignment updated successfully!')
            
        except Tire.DoesNotExist:
            messages.error(request, 'Selected tire does not exist!')
        except TirePosition.DoesNotExist:
            messages.error(request, 'Selected position does not exist!')
        except WorkOrder.DoesNotExist:
            messages.error(request, 'Selected work order does not exist!')
        except TireInspection.DoesNotExist:
            messages.error(request, 'Selected inspection does not exist!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('tire_assignment_list')