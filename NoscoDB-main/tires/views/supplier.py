from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import Supplier
# Supplier Views ------------------------------------------------------------------------------------------------------

def supplier_list(request):
    suppliers = Supplier.objects.all()
    
    context = {
        'suppliers': suppliers
    }
    return render(request, 'suppliers/supplier_list.html', context)

def supplier_delete(request, id):
    if request.method == 'POST':
        supplier = get_object_or_404(Supplier, id=id)
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
    return redirect('supplier_list')

def supplier_create(request):
    if request.method == 'POST':

        # Get data from the form
        supplier_name = request.POST.get('supplier_name')
        contact_person = request.POST.get('contact_person')
        phone = request.POST.get('phone')
        position = request.POST.get('position')
        email = request.POST.get('email')
        address = request.POST.get('address')
        evaluation = request.POST.get('evaluation')


        
        # Create the supplier
        supplier = Supplier.objects.create(
            supplier_name=supplier_name,
            contact_person=contact_person,
            phone=phone,
            position=position,
            email=email,
            address=address,
            evaluation=evaluation,
        )
        
        messages.success(request, 'Supplier created successfully!')
    
    return redirect('supplier_list')

def supplier_update(request, id):

    supplier = Supplier.objects.get(id=id)
    if request.method == 'POST':

        new_supplier_name = request.POST.get('supplier_name')

        # Update data
        supplier.supplier_name = new_supplier_name
        supplier.contact_person = request.POST.get('contact_person')
        supplier.phone = request.POST.get('phone')
        supplier.position = request.POST.get('position')
        supplier.email = request.POST.get('email')
        supplier.address = request.POST.get('address')
        supplier.evaluation = request.POST.get('evaluation')
        supplier.save()
        
        messages.success(request, 'Supplier updated successfully!')
    
    return redirect('supplier_list')


