from django.shortcuts import render
from ..models import Vehicle,Employee


# Menu Views
def menu_page(request):
    vehicles = Vehicle.objects.all()
    employees = Employee.objects.all()
    context = {
        'vehicles':vehicles,
        'employees':employees,
    }
    return render(request, 'menu/menu_page.html',context)
