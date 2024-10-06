from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import (
  login_required, permission_required
)
from django.shortcuts import render

from .. import models


@login_required
@permission_required('employees.view_employee')
def male_female_card(request: HttpRequest) -> HttpResponse:
    
    counts = models.Employee.objects.get_male_female_count()
    template_name = 'apps/employees/partials/dashboard/male-female-count.html'

    context = {'counts': counts}

    return render(request, template_name, context)