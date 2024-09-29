from apps.departments.models import Department


def run() -> None:

    primries = Department.objects.filter()
    print(primries)