from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import TireAssignment, Tire, TirePosition, TireInspection, WorkOrder
# Tire Assignment Views ------------------------------------------------------------------------------------------------------
def tire_assignment_list(request):
    tire_assignments = TireAssignment.objects.all()
    tires = Tire.objects.all()
    tire_positions = TirePosition.objects.all()
    tire_inspections = TireInspection.objects.all()
    
    # Handle work order
    work_order_id = request.GET.get('work_order', '')
    work_order = None
    if work_order_id:
        try:
            work_order = WorkOrder.objects.get(id=work_order_id)
        except WorkOrder.DoesNotExist:
            work_order = None
    
    # Initialize filtered querysets
    filtered_tires = Tire.objects.none()
    filtered_positions = TirePosition.objects.none()
    filtered_inspections = TireInspection.objects.none()
    
    if work_order:
        # Get the vehicle from work order
        vehicle = work_order.vehicle
        
        # 1. Filter tires: Tires currently mounted on this vehicle
        mounted_tire_ids = TirePosition.objects.filter(
            vehicle=vehicle, 
            mounted_tire__isnull=False
        ).values_list('mounted_tire_id', flat=True)
        filtered_tires = Tire.objects.filter(id__in=mounted_tire_ids)
        
        # 2. Filter positions: All positions for this vehicle
        filtered_positions = TirePosition.objects.filter(vehicle=vehicle)
        
        # 3. Filter inspections: Inspections for this vehicle's tires
        filtered_inspections = TireInspection.objects.filter(
            tire__in=filtered_tires
        ).order_by('-inspection_odometer')
    
    context = {
        'tire_assignments': tire_assignments,
        'tires': filtered_tires,
        'tire_positions': filtered_positions,
        'work_order': work_order,
        'tire_inspections': filtered_inspections,
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
        # Get data from the form
        tire_id = request.POST.get('tire')
        tire_position_from_id = request.POST.get('tire_position_from')
        tire_position_to_id = request.POST.get('tire_position_to')
        work_order_id = request.POST.get('work_order')
        tire_inspection_id = request.POST.get('tire_inspection')
        assignment_date = request.POST.get('assignment_date')
        removal_date = request.POST.get('removal_date')
        reason_for_removal = request.POST.get('reason_for_removal')

        tire = get_object_or_404(Tire, id=tire_id)
        tire_position_from = get_object_or_404(TirePosition, id=tire_position_from_id)
        tire_position_to = get_object_or_404(TirePosition, id=tire_position_to_id)
        work_order = get_object_or_404(WorkOrder, id=work_order_id)
        tire_inspection = get_object_or_404(TireInspection, id=tire_inspection_id)
        
        # Create the tire assignment
        tire_assignment = TireAssignment.objects.create(
            tire=tire,
            tire_position_from=tire_position_from,
            tire_position_to=tire_position_to,
            assignment_date=assignment_date,
            removal_date=removal_date,
            work_order=work_order,
            inspection=tire_inspection,
            reason_for_removal=reason_for_removal,
        )
        
        messages.success(request, 'Tire assignment created successfully!')
    return redirect('tire_assignment_list')
    
def tire_assignment_update(request, id):
    tire_assignment = get_object_or_404(TireAssignment, id=id)
    if request.method == 'POST':
        # Get data from the form
        tire_id = request.POST.get('tire')
        tire_position_from_id = request.POST.get('tire_position_from')
        tire_position_to_id = request.POST.get('tire_position_to')
        work_order_id = request.POST.get('work_order')
        tire_inspection_id = request.POST.get('tire_inspection')
        assignment_date = request.POST.get('assignment_date')
        removal_date = request.POST.get('removal_date')
        reason_for_removal = request.POST.get('reason_for_removal')

        tire = Tire.objects.get(id=tire_id)
        tire_position_from = TirePosition.objects.get(id=tire_position_from_id)
        tire_position_to = TirePosition.objects.get(id=tire_position_to_id)
        work_order = WorkOrder.objects.get(id=work_order_id)
        tire_inspection = TireInspection.objects.get(id=tire_inspection_id)

        # Update the tire assignment
        tire_assignment.tire = tire
        tire_assignment.tire_position_from = tire_position_from
        tire_assignment.tire_position_to = tire_position_to
        tire_assignment.assignment_date = assignment_date
        tire_assignment.removal_date = removal_date
        tire_assignment.work_order = work_order
        tire_assignment.inspection = tire_inspection
        tire_assignment.reason_for_removal = reason_for_removal
        tire_assignment.save()

        messages.success(request, 'Tire assignment updated successfully!')
    return redirect('tire_assignment_list')