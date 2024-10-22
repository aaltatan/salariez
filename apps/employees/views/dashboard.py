import json

from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import (
  login_required, permission_required
)
from django.shortcuts import render

from ..models import Employee


@login_required
@permission_required('employees.view_employee')
def male_female_card(request: HttpRequest) -> HttpResponse:
    
    counts = Employee.objects.get_male_female_count()
    template_name = 'apps/employees/partials/dashboard/male-female-count.html'

    context = {'data': json.dumps(counts)}

    return render(request, template_name, context)