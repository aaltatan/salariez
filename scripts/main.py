from apps.departments.models import Department


def run() -> None:

    parent = Department.objects.get(id=97)
    ans = parent.get_descendants()
    print(ans)