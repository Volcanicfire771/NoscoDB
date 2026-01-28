# tires/views/__init__.py

from .employee import *
from .maintainance_record import *
from .menu import *
from .service_type import *
from .supplier import *
from .tire_assignment import *
from .tire_inspection import *
from .tire_pattern import *
from .tire_position import *
from .tire_status import *
from .tires import *
from .vehicles import *
from .work_order import *
from .tire_wear import *

try:
    from .excel_import_new import (
        import_excel_upload,
        import_excel_mapping,
        import_excel_preview,
        import_excel_execute,
        import_excel_success,
    )
except ImportError:
    pass
