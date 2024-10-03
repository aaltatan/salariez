from django.core.management.base import BaseCommand

from ...utils import delete_unlinked_images


class Command(BaseCommand):
  
    help = "delete unlinked images from media directory"

    def handle(self, *args, **kwargs) -> None:
        delete_unlinked_images('profiles')