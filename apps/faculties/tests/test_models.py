from django.test import TestCase
from django.utils.text import slugify

from .. import models


class TestFaculty(TestCase):
    
    def setUp(self) -> None:
        objs = [
            models.Faculty(name='طب الأسنان', slug='الطب-البشري'),
            models.Faculty(name='الطب البشري', slug='الطب-البشري'),
            models.Faculty(name='xxxx', slug='الطب-البشري'),
            models.Faculty(name='الصيدلة'),
        ]
        for obj in objs:
            obj.save()
    
    def test_slugify(self):
        
        obj = models.Faculty.objects.filter(name__contains='سنان').first()
        self.assertEqual(obj.slug, 'الطب-البشري')
        obj = models.Faculty.objects.filter(name__contains='بشري').first()
        self.assertEqual(obj.slug, 'الطب-البشري-1')
        obj = models.Faculty.objects.filter(name__contains='xxx').first()
        self.assertEqual(obj.slug, 'الطب-البشري-2')
        obj = models.Faculty.objects.filter(name__contains='صيد').first()
        self.assertEqual(obj.slug, slugify(obj.name, allow_unicode=True))