# tables.py
import django_tables2 as tables
from .models import contactEnquiry

class StudentTable(tables.Table):
    class Meta:
        model = contactEnquiry
        template_name = 'django_tables2/bootstrap-responsive.html'  # Use a Bootstrap template
        attrs = {'class': 'table table-bordered table-hover'}
