# views.py (tire_assignment views)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from ..models import TireAssignment, Tire, Vehicle, TirePosition, TireInspection, WorkOrder, TireStatus

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
    
    # UNMOUNTED tires (for new mount option)
    unmounted_tires = Tire.objects.filter(
        current_position__isnull=True,  # Not mounted anywhere
        # is_scrapped=False  # Not scrapped
    ).select_related('status').order_by('serial_number')
    
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
        'unmounted_tires': unmounted_tires,  # NEW
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


@transaction.atomic
def tire_assignment_create(request):
    if request.method == 'POST':
        try:
            # Get all data from form
            tire_id = request.POST.get('tire')
            from_position_value = request.POST.get('tire_position_from')
            to_position_value = request.POST.get('tire_position_to')
            work_order_id = request.POST.get('work_order')
            inspection_id = request.POST.get('inspection')
            start_odometer = request.POST.get('start_odometer')
            end_odometer = request.POST.get('end_odometer')
            removal_mileage = request.POST.get('removal_mileage')
            assignment_date = request.POST.get('assignment_date')
            removal_date = request.POST.get('removal_date')
            reason_for_removal = request.POST.get('reason_for_removal')
            notes = request.POST.get('notes')
            
            # Debug print
            print("=== FORM DATA ===")
            print(f"to_position_value: {to_position_value}")
            print(f"discard_flag: {request.POST.get('discard_flag')}")
            print("=================")
            
            # Check if this is a DISCARD operation
            # Method 1: Check the hidden discard_flag
            discard_flag = request.POST.get('discard_flag')
            # Method 2: Check if to_position is "DISCARD"
            is_discard_from_value = (to_position_value == 'DISCARD')
            # Method 3: Final decision
            is_discard = (discard_flag == 'true' or is_discard_from_value)
            
            print(f"DEBUG: is_discard = {is_discard}")
            
            # Get or set default assignment date
            if not assignment_date:
                assignment_date = timezone.now().date()
            
            # Check if this is a NEW MOUNT operation
            is_new_mount = (from_position_value == 'NEW_MOUNT')
            
            # ====== SIMPLIFIED LOGIC ======
            
            # Get work order (required for all operations)
            work_order = WorkOrder.objects.get(id=work_order_id)
            
            # Get inspection if provided
            inspection = TireInspection.objects.get(id=inspection_id) if inspection_id else None
            
            # Initialize variables
            tire = None
            from_position = None
            to_position = None
            
            # Handle discard operation FIRST
            if is_discard:
                print("DEBUG: Processing DISCARD operation")
                
                # For discard, we need tire and from_position
                tire = Tire.objects.get(id=tire_id)
                from_position = TirePosition.objects.get(id=from_position_value) if from_position_value else None
                
                # Validate
                if not from_position:
                    messages.error(request, 'Please select a position to discard from!')
                    return redirect('tire_assignment_list')
                
                if not reason_for_removal:
                    messages.error(request, 'Please provide a reason for discarding the tire.')
                    return redirect('tire_assignment_list')
                
                # Check tire is in from_position
                if from_position.mounted_tire != tire:
                    messages.error(request, 'Selected tire is not in the source position!')
                    return redirect('tire_assignment_list')
                
                # to_position is None for discard
                to_position = None
                
            else:
                print("DEBUG: Processing NORMAL operation (move or mount)")
                
                # Handle tire selection
                if is_new_mount:
                    # For new mount, get tire from new_tire_select field
                    tire_id = request.POST.get('new_tire_select')
                    if not tire_id:
                        messages.error(request, 'Please select a tire to mount')
                        return redirect('tire_assignment_list')
                    tire = Tire.objects.get(id=tire_id)
                    from_position = None  # No from position for new mount
                else:
                    # Normal move
                    tire = Tire.objects.get(id=tire_id)
                    from_position = TirePosition.objects.get(id=from_position_value) if from_position_value else None
                
                # Validate tire is in from_position (for moves, not new mounts)
                if not is_new_mount and from_position and from_position.mounted_tire != tire:
                    messages.error(request, 'Selected tire is not in the source position!')
                    return redirect('tire_assignment_list')
                
                # Get to_position for normal operations
                # IMPORTANT: to_position_value should be a valid position ID, not "DISCARD"
                to_position = TirePosition.objects.get(id=to_position_value)
                
                # Check to_position is empty
                if to_position.mounted_tire is not None:
                    messages.error(request, 'Target position is not empty!')
                    return redirect('tire_assignment_list')
            
            # ====== CREATE THE ASSIGNMENT ======
            tire_assignment = TireAssignment.objects.create(
                tire=tire,
                tire_position_from=from_position,
                tire_position_to=to_position,  # None for discard
                work_order=work_order,
                inspection=inspection,
                assignment_date=assignment_date,
                start_odometer=start_odometer,
                end_odometer=end_odometer if end_odometer else None,
                removal_mileage=removal_mileage if removal_mileage else None,
                removal_date=removal_date if removal_date else None,
                reason_for_removal=reason_for_removal if reason_for_removal else '',
                notes=notes if notes else '',
                is_discard_operation=is_discard,
            )
            
            print(f"DEBUG: Assignment created with is_discard_operation = {is_discard}")
            
            # ====== PROCESS BASED ON OPERATION TYPE ======
            if is_discard:
                # DISCARD: Mark tire as scrapped
                discarded_status, created = TireStatus.objects.get_or_create(
                    status_name="DISCARDED",
                    defaults={'description': 'Tire has been discarded'}
                )
                
                tire.status = discarded_status
                # tire.is_scrapped = True
                tire.current_position = None
                # tire.current_vehicle = None
                tire.save()
                
                # Clear the position
                if from_position:
                    from_position.mounted_tire = None
                    from_position.save()
                
                messages.success(request, f'Tire {tire.serial_number} has been discarded and marked as scrapped.')
                
            else:
                # NORMAL MOVE or MOUNT
                # Remove from old position (if any)
                if from_position:
                    from_position.mounted_tire = None
                    from_position.save()
                
                # Mount to new position
                to_position.mounted_tire = tire
                to_position.save()
                
                # Update tire
                tire.current_position = to_position
                # tire.current_vehicle = to_position.vehicle
                
                # Update tire status
                if tire.status.status_name == 'READY':
                    mounted_status, created = TireStatus.objects.get_or_create(
                        status_name="MOUNTED",
                        defaults={'description': 'Currently mounted'}
                    )
                    tire.status = mounted_status
                
                tire.save()
                
                # Update inspections
                if inspection:
                    inspection.position = to_position
                    inspection.work_order = work_order
                    inspection.save()
                
                if from_position:
                    TireInspection.objects.filter(
                        tire=tire,
                        position=from_position
                    ).update(position=to_position)
                
                if is_new_mount:
                    messages.success(request, f'Tire {tire.serial_number} mounted successfully!')
                else:
                    messages.success(request, f'Tire {tire.serial_number} moved successfully!')
            
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
            print(f"DEBUG: Exception: {str(e)}")
            import traceback
            traceback.print_exc()
    
    return redirect('tire_assignment_list')

def tire_assignment_update(request, id):
    tire_assignment = get_object_or_404(TireAssignment, id=id)
    
    # Prevent editing discard operations
    if tire_assignment.is_discard():
        messages.error(request, 'Discard operations cannot be edited!')
        return redirect('tire_assignment_list')
    
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
            inspection_id = request.POST.get('inspection')
            assignment_date = request.POST.get('assignment_date')
            removal_date = request.POST.get('removal_date')
            reason_for_removal = request.POST.get('reason_for_removal')
            start_odometer = request.POST.get('start_odometer')
            end_odometer = request.POST.get('end_odometer')
            removal_mileage = request.POST.get('removal_mileage')
            
            # Get objects
            tire = Tire.objects.get(id=tire_id)
            tire_position_from = TirePosition.objects.get(id=tire_position_from_id) if tire_position_from_id else None
            tire_position_to = TirePosition.objects.get(id=tire_position_to_id)
            work_order = WorkOrder.objects.get(id=work_order_id)
            inspection = TireInspection.objects.get(id=inspection_id) if inspection_id else None
            
            # VALIDATIONS
            # Check if tire can be assigned
            # if tire.is_scrapped:
            #     messages.error(request, 'This tire is scrapped and cannot be assigned!')
            #     return redirect('tire_assignment_list')
            
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
            tire_assignment.start_odometer = start_odometer
            tire_assignment.end_odometer = end_odometer if end_odometer else None
            tire_assignment.removal_mileage = removal_mileage if removal_mileage else None
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