import os
from pathlib import Path

from django.conf import settings

from .models.employee import Employee

from apps.base.utils import views


class Deleter(views.Deleter):

    def can_delete_criteria(self) -> bool:
        return True


def delete_unlinked_images(directory: str) -> None:
    employees = Employee.objects.all()
    images_db = [
        e.profile.name.replace(f'{directory}/', '') 
        for e in employees 
        if e.profile.name
    ]

    media_root: Path = settings.MEDIA_ROOT

    images_os = os.listdir(media_root / directory)
    unlinked_images = set(images_db) ^ set(images_os)
    
    for image in unlinked_images:
        image_path = media_root / directory / image 
        image_path.unlink(missing_ok=True)
    
    print(f'{len(unlinked_images)} images(s) has been deleted successfully')