import json

from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import (
  login_required, permission_required
)
from django.shortcuts import render

from ..models import Employee


@login_required
@permission_required('employees.view_employee')
def counts_card(
    request: HttpRequest, group_by: str = 'gender'
) -> HttpResponse:
    
    counts = Employee.objects.get_counts_grouped_by(group_by)
    template_name = \
        'apps/employees/partials/dashboard/group-by-counts.html'
    context = {'data': json.dumps(list(counts))}

    return render(request, template_name, context)