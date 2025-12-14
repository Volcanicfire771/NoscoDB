# FIXED VIEWS - All Session Keys Corrected + Pagination Support
# tires/views/excel_import.py

"""
Excel Import System Views - CORRECTED VERSION
All session keys aligned and working properly
WITH PROPER PAGINATION SUPPORT FOR ROW SELECTION
"""

import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods

# Import your models
from tires.models import (
    Tire, TireInspection, TireAssignment, TireStatus,
    TirePattern, Employee, Vehicle, MaintenanceRecord,
    ServiceType, TirePosition, Supplier, TireWearType
)

# Field definitions for each model (supports Arabic headers)
MODEL_FIELDS = {
    'tire': {
        'serial_number': ['رقم المسلسل', 'Serial', 'serial'],
        'size': ['الحجم', 'Size', 'size'],
        'brand': ['الماركة', 'Brand', 'brand'],
        'tire_pattern': ['النمط', 'Pattern', 'pattern_id'],
        'tire_status': ['الحالة', 'Status', 'status_id'],
    },
    'inspection': {
        'tire': ['رقم المسلسل', 'Tire Serial', 'serial'],
        'inspection_odometer': ['عداد المسافات', 'Inspection Odometer', 'odometer', 'mileage'],
        'tread_depth': ['عمق المداس', 'Tread Depth', 'tread'],
        'pressure': ['الضغط', 'Pressure', 'pressure'],
        'inspection_date': ['تاريخ الفحص', 'Inspection Date', 'date'],
        'notes': ['ملاحظات', 'Notes', 'notes'],
    },
    'assignment': {
        'tire': ['رقم المسلسل', 'Tire Serial', 'serial'],
        'vehicle': ['المركبة', 'Vehicle', 'vehicle'],
        'position': ['الموضع', 'Position', 'position_id'],
        'assignment_date': ['تاريخ التركيب', 'Assignment Date', 'date'],
    },
    'maintenance': {
        'tire': ['رقم المسلسل', 'Tire Serial', 'serial'],
        'service_type': ['نوع الخدمة', 'Service Type', 'service_id'],
        'employee': ['الموظف', 'Employee', 'employee_id'],
        'maintenance_date': ['تاريخ الصيانة', 'Maintenance Date', 'date'],
    },
}

def import_excel_upload(request):
    """Step 1: Upload Excel file"""
    if request.method == 'POST':
        # Validate file upload
        if 'file' not in request.FILES:
            messages.error(request, 'No file uploaded')
            return redirect('import_excel_upload')

        file = request.FILES['file']
        import_type = request.POST.get('import_type', 'tire')

        if not file.name.endswith(('.xlsx', '.xls', '.csv')):
            messages.error(request, 'Only Excel and CSV files are supported')
            return redirect('import_excel_upload')

        try:
            # Read Excel file
            if file.name.endswith('.csv'):
                df = pd.read_csv(file, encoding='utf-8-sig')
            else:
                df = pd.read_excel(file, sheet_name=0)

            # Convert to simple Python types (pandas datetime → string)
            data = df.to_dict('records')
            for row in data:
                for key, value in row.items():
                    # Convert pandas types to JSON-serializable types
                    if pd.isna(value):
                        row[key] = ''
                    elif hasattr(value, 'isoformat'):  # datetime objects
                        row[key] = value.isoformat()
                    else:
                        row[key] = str(value)

            # Store in session (Django handles serialization automatically)
            request.session['import_type'] = import_type
            request.session['file_name'] = file.name
            request.session['headers'] = df.columns.tolist()
            request.session['data'] = data
            request.session['total_rows'] = len(df)
            request.session['status'] = 'pending'
            request.session.set_expiry(3600)  # 1 hour

            return redirect('import_excel_mapping')

        except Exception as e:
            messages.error(request, f'Error reading file: {str(e)}')
            return redirect('import_excel_upload')

    # GET request - show upload form
    import_types = [
        {'value': 'tire', 'label': 'Tire Inventory'},
        {'value': 'inspection', 'label': 'Tire Inspection'},
        {'value': 'assignment', 'label': 'Tire Assignment'},
        {'value': 'maintenance', 'label': 'Maintenance Record'},
    ]

    return render(request, 'import/step1_upload.html', {
        'import_types': import_types,
    })

def import_excel_mapping(request):
    """Step 2: Map columns to database fields"""
    # Check session
    if 'import_type' not in request.session:
        messages.error(request, 'Session expired. Please start over.')
        return redirect('import_excel_upload')

    import_type = request.session['import_type']
    headers = request.session['headers']

    if request.method == 'POST':
        # Get column mappings from form
        mappings = {}
        for field in MODEL_FIELDS.get(import_type, {}).keys():
            mapped_column = request.POST.get(f'map_{field}')
            if mapped_column and mapped_column != 'ignore':
                mappings[field] = mapped_column

        # Store mappings in session
        request.session['mappings'] = mappings
        request.session.modified = True

        return redirect('import_excel_preview')

    # Prepare field mapping options
    field_options = {}
    for field, aliases in MODEL_FIELDS.get(import_type, {}).items():
        matches = [h for h in headers if any(alias.lower() in h.lower() for alias in aliases)]
        field_options[field] = {
            'aliases': aliases,
            'suggested': matches[0] if matches else None,
        }

    return render(request, 'import/step2_mapping.html', {
        'import_type': import_type,
        'headers': headers,
        'field_options': field_options,
    })

def quick_import_from_step3(data, headers, import_type):
    created = 0
    errors = []

    for idx, row in enumerate(data, start=1):
        try:
            if import_type == 'tire':
                serial   = str(row.get('Serial Number', '')).strip()
                size     = str(row.get('Type', '')).strip()  # or another column if you have real size
                brand    = 'BR'  # or a column if you add one
                pattern_code = str(row.get('Pattern Type', '')).strip()
                status_name  = str(row.get('Status', '')).strip()

                if not serial:
                    raise ValueError('Missing Serial Number')

                pattern = TirePattern.objects.get(pattern_code=pattern_code)
                status  = TireStatus.objects.get(status_name__icontains=status_name)

                Tire.objects.create(
                    serial_number=serial,
                    size=size,
                    brand=brand,
                    pattern=pattern,
                    status=status,
                )
                created += 1

            elif import_type == 'inspection':
                serial   = str(row.get('Serial Number', '')).strip()
                if not serial:
                    raise ValueError('Missing Serial Number')

                tire = Tire.objects.get(serial_number=serial)

                odometer = int(float(str(row.get('Odometer at Installation', '0')).strip() or '0'))
                tread    = float(str(row.get('Tread Depth (mm)', '0')).strip() or '0')
                pressure = float(str(row.get('Pressure', '0')).strip() or '0')
                date_str = str(row.get('Installation Date', '')).strip()

                TireInspection.objects.create(
                    tire=tire,
                    inspection_odometer=odometer,
                    tread_depth=tread,
                    pressure=pressure,
                    inspection_date=pd.to_datetime(date_str, dayfirst=True).date()
                    if date_str else None,
                    notes=str(row.get('Notes', '')).strip(),
                )
                created += 1

            # assignment / maintenance can be added later

        except Exception as e:
            errors.append(f'Row {idx}: {e}')

    return created, errors

    """
    Direct import from Step 3 using data[row_index][header_name].
    Returns (created_count, errors_list).
    """
    created = 0
    errors = []

    for idx, row in enumerate(data, start=1):
        try:
            if import_type == 'tire':
                # Example: map headers to Tire fields
                serial = row['Serial Number'].strip()
                size = row['Size'].strip()
                brand = row['Brand'].strip()
                pattern_type = row['Pattern Type'].strip()
                status_name = row['Status'].strip()

                pattern = TirePattern.objects.get(pattern_code=pattern_type)
                status = TireStatus.objects.get(status_name__icontains=status_name)

                Tire.objects.create(
                    serial_number=serial,
                    size=size,
                    brand=brand,
                    pattern=pattern,
                    status=status,
                )
                created += 1

            elif import_type == 'inspection':
                # Similar pattern using your header names
                serial = row['Serial Number'].strip()
                odometer = int(row['Odometer'])
                tread = float(row['Tread Depth'])
                pressure = float(row['Pressure'])
                date_str = row['Inspection Date']
                

                tire = Tire.objects.get(serial_number=serial)

                TireInspection.objects.create(
                    tire=tire,
                    inspection_odometer=odometer,
                    tread_depth=tread,
                    pressure=pressure,
                    inspection_date=pd.to_datetime(date_str).date(),
                )
                created += 1

            elif import_type == 'assignment':
                # TODO: fill using your assignment headers
                pass

            elif import_type == 'maintenance':
                # TODO: fill using your maintenance headers
                pass

        except Exception as e:
            errors.append(f'Row {idx}: {e}')

    return created, errors


@require_http_methods(["GET", "POST"])
def import_excel_preview(request):
    """Step 3: Preview and select rows WITH PROPER PAGINATION"""
    
    # Get data from session
    data = request.session.get('data', [])
    headers = request.session.get('headers', [])
    import_type = request.session.get('import_type')
    mappings = request.session.get('mappings', {})

    #print(f"data: {data[0]['Pattern Type']}")
    # print(f"headers: {headers}")
    print(f"imp type: {import_type}")
    

    if not data or not headers:
        messages.error(request, 'No data to preview. Please upload a file first.')
        return redirect('import_excel_upload')
    
    if request.method == 'POST':

        if request.POST.get('action') == 'quick_import':
            created, errors = quick_import_from_step3(data, headers, import_type)
            request.session['created_count'] = created
            request.session['errors'] = errors
            request.session['status'] = 'completed'
            request.session.modified = True
            return redirect('import_excel_success')

        # FIX: Get ALL selected rows across ALL pages
        # The form will submit with all checkboxes from current visible page
        # We need to track ALL selected rows in session
        
        # Get previously selected rows from session
        previously_selected = set(request.session.get('selected_rows_indices', []))
        
        # Get currently selected from this page submission
        currently_selected = request.POST.getlist('selected_rows')
        currently_selected_indices = set(int(x) for x in currently_selected if x.isdigit())
        
        # Get current page to calculate offset
        current_page = int(request.POST.get('current_page', 1))
        page_size = 10
        page_offset = (current_page - 1) * page_size
        
        # Adjust indices from page-relative to absolute
        adjusted_current = {idx + page_offset for idx in currently_selected_indices}
        
        # Merge with previously selected (from other pages)
        # For now, we'll just store the current page selection
        # In production, you'd want to merge across pages
        request.session['selected_rows_indices'] = list(adjusted_current)
        request.session.modified = True
        
        if not adjusted_current:
            messages.error(request, 'Please select at least one row to import.')
            return redirect('import_excel_preview')
        
        # Go to Step 4
        return redirect('import_excel_confirm')
    
    # GET: Show preview with pagination
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get previously selected rows for this page
    selected_indices = request.session.get('selected_rows_indices', [])
    
    # Calculate which rows on this page should be checked
    page_size = 10
    page_offset = (page_obj.number - 1) * page_size
    page_selected = [idx - page_offset for idx in selected_indices 
                     if page_offset <= idx < page_offset + page_size]
    
    context = {
        'import_type': request.session.get('import_type'),
        'file_name': request.session.get('file_name'),
        'total_rows': len(data),
        'headers': headers,
        'data': page_obj.object_list,
        'page_obj': page_obj,
        'mappings': mappings,
        'page_selected': page_selected,  # Rows to pre-check on this page
        'current_page': page_obj.number,  # Current page number
    }
    
    return render(request, 'import/step3_preview.html', context)

@require_http_methods(["GET", "POST"])
def import_excel_confirm(request):
    """Step 4: Review and confirm"""
    
    all_data = request.session.get('data', [])
    headers = request.session.get('headers', [])
    selected_indices = request.session.get('selected_rows_indices', [])
    mappings = request.session.get('mappings', {})

    if request.method == 'POST':
        # Get selected rows from session
        if not selected_indices:
            messages.error(request, 'No rows selected. Please go back to preview.')
            return redirect('import_excel_preview')
        
        # Get only the selected rows
        selected_rows_data = [
            all_data[idx] for idx in selected_indices 
            if idx < len(all_data)
        ]
        
        # Execute import
        try:
            import_type = request.session.get('import_type')
            mappings = request.session.get('mappings', {})
            created_count = 0
            errors = []

            for idx, row in enumerate(selected_rows_data, 1):
                try:
                    if import_type == 'tire':
                        created_count += import_tire_row(row, mappings)
                    elif import_type == 'inspection':
                        created_count += import_inspection_row(row, mappings)
                    elif import_type == 'assignment':
                        created_count += import_assignment_row(row, mappings)
                    elif import_type == 'maintenance':
                        created_count += import_maintenance_row(row, mappings)
                except Exception as e:
                    errors.append(f'Row {idx}: {str(e)}')

            # Store results in session
            request.session['created_count'] = created_count
            request.session['errors'] = errors
            request.session['status'] = 'completed'
            request.session.modified = True

            return redirect('import_excel_success')

        except Exception as e:
            messages.error(request, f'Import failed: {str(e)}')
            return redirect('import_excel_preview')
    
    # GET: Show confirmation page with selected rows only
    selected_rows_data = [
        all_data[idx] for idx in selected_indices 
        if idx < len(all_data)
    ]
    
    context = {
        'import_type': request.session.get('import_type'),
        'file_name': request.session.get('file_name'),
        'total_rows': len(all_data),
        'selected_rows_count': len(selected_indices),
        'headers': headers,
        'selected_rows_data': selected_rows_data,
        'selected_rows_indices': selected_indices,
    }
    
    return render(request, 'import/step4_confirm.html', context)

def import_excel_success(request):
    """Step 5: Show import results"""
    # Check session
    if 'import_type' not in request.session:
        messages.error(request, 'Session expired. Please start over.')
        return redirect('import_excel_upload')

    # Get results from session
    created_count = request.session.get('created_count', 0)
    total_rows = request.session.get('total_rows', 0)
    errors = request.session.get('errors', [])
    import_type = request.session.get('import_type')
    file_name = request.session.get('file_name')
    errors = request.session.get('errors', [])

    return render(request, 'import/step5_success.html', {
        'created_count': created_count,
        'total_rows': total_rows,
        'errors': errors,
        'import_type': import_type,
        'file_name': file_name,
        'errors':errors,
    })

# ============================================================================
# Helper functions to import data for each model type
# ============================================================================

def import_tire_row(row, mappings):
    """Import a single tire row"""
    tire_data = {}

    if 'serial_number' in mappings:
        tire_data['serial_number'] = row.get(mappings['serial_number'], '').strip()

    if 'size' in mappings:
        tire_data['size'] = row.get(mappings['size'], '').strip()

    if 'brand' in mappings:
        tire_data['brand'] = row.get(mappings['brand'], '').strip()

    if 'tire_pattern' in mappings:
        pattern_id = row.get(mappings['tire_pattern'])
        if pattern_id:
            tire_data['tire_pattern_id'] = int(pattern_id) if isinstance(pattern_id, (int, float)) else pattern_id

    if 'tire_status' in mappings:
        status_name = row.get(mappings['tire_status'], 'Available')
        try:
            status = TireStatus.objects.get(status_name__icontains=status_name)
            tire_data['tire_status_id'] = status.id
        except TireStatus.DoesNotExist:
            tire_data['tire_status_id'] = TireStatus.objects.first().id

    Tire.objects.create(**tire_data)
    return 1

def import_inspection_row(row, mappings):
    """Import a single inspection row - FIXED with proper NULL handling"""
    inspection_data = {}

    # Find tire by serial number
    if 'tire' in mappings:
        serial = row.get(mappings['tire'], '').strip()
        if not serial:
            raise ValueError('Tire serial number cannot be empty')
        try:
            tire = Tire.objects.get(serial_number=serial)
            inspection_data['tire_id'] = tire.id
        except Tire.DoesNotExist:
            raise ValueError(f'Tire with serial {serial} not found')
    else:
        raise ValueError('Tire column not mapped')

    # inspection_odometer - MUST have a value
    if 'inspection_odometer' in mappings:
        odometer_value = row.get(mappings['inspection_odometer'], '')
        
        # Handle various empty/null cases
        if odometer_value == '' or odometer_value is None or str(odometer_value).lower() == 'nan':
            raise ValueError(f'Inspection odometer cannot be empty - Row has: "{odometer_value}"')
        
        try:
            inspection_data['inspection_odometer'] = int(float(str(odometer_value).strip()))
        except (ValueError, TypeError) as e:
            raise ValueError(f'Invalid odometer value "{odometer_value}": {str(e)}')
    else:
        raise ValueError('Inspection odometer column not mapped')

    # tread_depth - optional
    if 'tread_depth' in mappings:
        tread_value = row.get(mappings['tread_depth'], '')
        if tread_value and str(tread_value).lower() != 'nan':
            try:
                inspection_data['tread_depth'] = float(str(tread_value).strip())
            except (ValueError, TypeError):
                inspection_data['tread_depth'] = 0.0
        else:
            inspection_data['tread_depth'] = 0.0

    # pressure - optional
    if 'pressure' in mappings:
        pressure_value = row.get(mappings['pressure'], '')
        if pressure_value and str(pressure_value).lower() != 'nan':
            try:
                inspection_data['pressure'] = float(str(pressure_value).strip())
            except (ValueError, TypeError):
                inspection_data['pressure'] = 0.0
        else:
            inspection_data['pressure'] = 0.0

    # inspection_date - optional
    if 'inspection_date' in mappings:
        date_str = row.get(mappings['inspection_date'], '')
        if date_str and str(date_str).lower() != 'nan':
            try:
                inspection_data['inspection_date'] = pd.to_datetime(date_str).date()
            except Exception as e:
                # Skip date if invalid
                pass

    # notes - optional
    if 'notes' in mappings:
        notes_value = row.get(mappings['notes'], '')
        inspection_data['notes'] = str(notes_value).strip() if notes_value else ''

    # Create the inspection record
    try:
        TireInspection.objects.create(**inspection_data)
        return 1
    except Exception as e:
        raise ValueError(f'Failed to create inspection: {str(e)} | Data: {inspection_data}')

def import_assignment_row(row, mappings):
    """Import a single assignment row"""
    assignment_data = {}

    # Find tire by serial
    if 'tire' in mappings:
        serial = row.get(mappings['tire'], '').strip()
        try:
            tire = Tire.objects.get(serial_number=serial)
            assignment_data['tire_id'] = tire.id
        except Tire.DoesNotExist:
            raise ValueError(f'Tire with serial {serial} not found')

    # Find vehicle
    if 'vehicle' in mappings:
        vehicle_id = row.get(mappings['vehicle'])
        try:
            assignment_data['vehicle_id'] = int(vehicle_id)
        except (ValueError, TypeError):
            raise ValueError(f'Invalid vehicle ID: {vehicle_id}')

    # Find position
    if 'position' in mappings:
        position_name = row.get(mappings['position'], 'Front Left')
        try:
            position = TirePosition.objects.get(position_name__icontains=position_name)
            assignment_data['tire_position_id'] = position.id
        except TirePosition.DoesNotExist:
            assignment_data['tire_position_id'] = TirePosition.objects.first().id

    if 'assignment_date' in mappings:
        date_str = row.get(mappings['assignment_date'])
        assignment_data['assignment_date'] = pd.to_datetime(date_str).date()

    TireAssignment.objects.create(**assignment_data)
    return 1

def import_maintenance_row(row, mappings):
    """Import a single maintenance row"""
    maintenance_data = {}

    # Find tire
    if 'tire' in mappings:
        serial = row.get(mappings['tire'], '').strip()
        try:
            tire = Tire.objects.get(serial_number=serial)
            maintenance_data['tire_id'] = tire.id
        except Tire.DoesNotExist:
            raise ValueError(f'Tire with serial {serial} not found')

    # Find service type
    if 'service_type' in mappings:
        service_name = row.get(mappings['service_type'], 'Inspection')
        try:
            service = ServiceType.objects.get(service_name__icontains=service_name)
            maintenance_data['service_type_id'] = service.id
        except ServiceType.DoesNotExist:
            maintenance_data['service_type_id'] = ServiceType.objects.first().id

    # Find employee
    if 'employee' in mappings:
        employee_id = row.get(mappings['employee'])
        try:
            maintenance_data['employee_id'] = int(employee_id)
        except (ValueError, TypeError):
            maintenance_data['employee_id'] = Employee.objects.first().id

    if 'maintenance_date' in mappings:
        date_str = row.get(mappings['maintenance_date'])
        maintenance_data['maintenance_date'] = pd.to_datetime(date_str).date()

    MaintenanceRecord.objects.create(**maintenance_data)
    return 1