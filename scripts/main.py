from apps.cities.models import City


def run() -> None:

    obj = City.objects.first()
    old_data = obj.__dict__
    del old_data['_state']
    print(old_data)