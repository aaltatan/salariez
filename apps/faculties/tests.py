from django.test import TestCase
from django.utils.text import slugify

from . import models

# Create your tests here.
class TestFaculty(TestCase):
    
    # def setUp(self) -> None:
    #     objs = [
    #         models.Faculty(name='طب الأسنان'),
    #         models.Faculty(name='الطب البشري'),
    #     ]
    #     models.Faculty.objects.bulk_create(objs)
        
    
    def test_slugify(self):
        
        obj = models.Faculty.objects.first()
        self.assertEqual(obj.slug, slugify(obj.name))