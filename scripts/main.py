from icecream import ic

from apps.departments.models import Department


def run() -> None:
  qs = Department.objects.first()
  ic(qs.search)