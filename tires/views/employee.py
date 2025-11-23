from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import Employee

# Employee Views ------------------------------------------------------------------------------------------------------

def employee_list(request):
    employees = Employee.objects.all()
    
    context = {
        'employees': employees
    }
    # # Get filter parameters from request
    # status_filter = request.GET.get('status_filter', '')
    # type_filter = request.GET.get('type_filter', '')
    # year_filter = request.GET.get('year_filter', '')
    
    # # Apply filters
    # if status_filter:
    #     employees = employees.filter(status=status_filter)
    # if type_filter:
    #     employees = employees.filter(employee_type=type_filter)
    # if year_filter:
    #     employees = employees.filter(year=year_filter)
    
    # context = {
    #     'employees': employees,
    #     'status_filter': status_filter,
    #     'type_filter': type_filter,
    #     'year_filter': year_filter,
    # }
    return render(request, 'employees/employee_list.html', context)

def employee_delete(request, id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=id)
        employee.delete()
        messages.success(request, 'employee deleted successfully!')
    return redirect('employee_list')

def employee_create(request):
    if request.method == 'POST':

        # Get data from the form
        employment_code = request.POST.get('employment_code')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        position = request.POST.get('position')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')

        
        # Validations

        # Validate license plate uniqueness
        if Employee.objects.filter(employment_code=employment_code).exists():
            messages.error(request, 'employee already exists!')
            return redirect('employee_list')
        
        # Create the employee
        employee = Employee.objects.create(
            employment_code=employment_code,
            first_name=first_name,
            last_name=last_name,
            position=position,
            email=email,
            contact_number=contact_number,
        )
        
        messages.success(request, 'Employee created successfully!')
    
    return redirect('employee_list')

def employee_update(request, id):

    employee = Employee.objects.get(id=id)
    if request.method == 'POST':

        new_employment_code = request.POST.get('employment_code')
        
        # Validations

        # Validate license plate uniqueness
        if Employee.objects.filter(employment_code=new_employment_code).exclude(id=id).exists():
            messages.error(request, 'employee code already exists!')
            return redirect('employee_list')
        
        # Update data
        employee.employment_code = new_employment_code
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.position = request.POST.get('position')
        employee.email = request.POST.get('email')
        employee.contact_number = request.POST.get('contact_number')
        
        employee.save()
        
        messages.success(request, 'Employee updated successfully!')
    
    return redirect('employee_list')


