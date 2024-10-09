from apps.departments.models import Department

def run() -> None:

    obj = Department.objects.filter(name__contains='رواتب').first()
    print(obj.get_ancestors(include_self=True))