from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import WorkOrder, Employee, Vehicle

# Work Orders Views ------------------------------------------------------------------------------------------------------

def work_order_list(request):
    work_orders = WorkOrder.objects.all()
    employees = Employee.objects.all()
    vehicles = Vehicle.objects.all()
    context = {
        'work_orders': work_orders,
        'employees': employees,
        'vehicles': vehicles
    }
    
    return render(request, 'work_orders/work_order_list.html', context)

def work_order_delete(request, id):
    if request.method == 'POST':
        work_order = get_object_or_404(WorkOrder, id=id)
        work_order.delete()
        messages.success(request, 'Work Order deleted successfully!')
    return redirect('work_order_list')

def work_order_create(request):
    if request.method == 'POST':

        # Get data from the form
        work_order_number = request.POST.get('work_order_number')
        date_created = request.POST.get('date_created')
        assigned_to_id = request.POST.get('assigned_to')
        vehicle_id = request.POST.get('vehicle')
        current_odometer = request.POST.get('current_odometer')
        shift_type = request.POST.get('shift_type')
        status = request.POST.get('status')
        # cost = request.POST.get('cost')
        
        assigned_to = Employee.objects.get(id=assigned_to_id)
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Validations

        # Validate work order number uniqueness
        if WorkOrder.objects.filter(work_order_number=work_order_number).exists():
            messages.error(request, 'Work order number already exists!')
            return redirect('work_order_list')
        
        # Validate that vehicle selected isn't in another open work order
        if WorkOrder.objects.filter(vehicle=vehicle,status="OPENED").exists():
            messages.error(request, 'There is another open Work order with this vehicle!')
            return redirect('work_order_list')

        # Create the work order
        work_order = WorkOrder.objects.create(
            work_order_number=work_order_number,
            assigned_to=assigned_to,
            vehicle=vehicle,
            current_odometer=current_odometer,
            shift_type=shift_type,
            status=status,
            # cost=cost
        )
        
        messages.success(request, 'Work Order created successfully!')
    
        
            

    return redirect('work_order_list')

def work_order_update(request, id):

    work_order = WorkOrder.objects.get(id=id)
    if request.method == 'POST':

        new_work_order_number = request.POST.get('work_order_number')
        assigned_to_id = request.POST.get('assigned_to')
        vehicle_id = request.POST.get('vehicle')
        
        assigned_to = Employee.objects.get(id=assigned_to_id)
        new_vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Validations

        # Validate work order number uniqueness
        if WorkOrder.objects.filter(work_order_number=new_work_order_number).exclude(id=id).exists():
            messages.error(request, 'Work order number already exists!')
            return redirect('work_order_list')
        
        # Validate that vehicle selected isn't in another open work order
        if WorkOrder.objects.filter(vehicle=new_vehicle,status="OPENED").exclude(id=id).exists():
            messages.error(request, 'There is another open Work order with this vehicle!')
            return redirect('work_order_list')

        # Update data
        work_order.work_order_number = new_work_order_number
        work_order.assigned_to = assigned_to
        work_order.vehicle = new_vehicle
        work_order.current_mileage = request.POST.get('current_mileage')
        work_order.shift_type = request.POST.get('shift_type')
        work_order.status = request.POST.get('status')
        work_order.cost = request.POST.get('cost')
        
        work_order.save()
        
        messages.success(request, 'Work Order updated successfully!')
    # return redirect(f'/tire-inspections/?vehicle_filter={vehicle_id}&create=true') #temp
    return redirect('work_order_list')

