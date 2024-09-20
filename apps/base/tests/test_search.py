from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.urls import reverse

from selectolax.parser import HTMLParser
from icecream import ic

from ...areas.models import Area, City


class TestSearch(TestCase):
    
    def setUp(self) -> None:
        user = User.objects.create_user(username='user', password='password')
        can_view_perm = Permission.objects.get(codename='view_area')
        user.user_permissions.add(can_view_perm)
        cities = [
            City(name='Hamah'),
            City(name='Homs'),
            City(name='Halab'),
        ]

        for c in cities:
            c.save()

        hama_gov = Area(name='hama gov', city=cities[0]).save()
        salamiah = Area(name='salamiah city', city=cities[0]).save()
        homs_gov = Area(name='homs gov', city=cities[1]).save()
        halab_gov = Area(name='halab gov', city=cities[2]).save()

    def test_areas_count(self):
        
        count = Area.objects.all().count()
        self.assertEqual(count, 4)

    def test_multiple(self):
        
        login = self.client.login(username='user', password='password')
        
        response = self.client.get(
            reverse('areas:index'),
            # QUERY_STRING='?name=&city=1&city=2&description=',
            headers={
                'Hx-Request': True,
            }
        )

        ic(response.content)

        parser = HTMLParser(response.content)
        rows = parser.css('table tbody tr')

        self.assertEqual(len(rows), 4)