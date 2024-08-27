from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission

from selectolax.parser import HTMLParser
from icecream import ic

from ..models import Faculty


class TestViews(TestCase):
    
    def setUp(self) -> None:
        
        self.parser = HTMLParser
        
        objs = [
            Faculty(name='dent'),
            Faculty(name='pharm'),
            Faculty(name='mang'),
            Faculty(name='civil'),
        ]
        for obj in objs:
            obj.save()
        
        delete_perm = Permission.objects.get(codename='delete_faculty')
        user_can_delete: User = (
            User.objects.create_user(username='user', password='password')
        )
        user_can_delete.user_permissions.add(delete_perm)
        
        view_perm = Permission.objects.get(codename='view_faculty')
        user_can_view: User = (
            User.objects.create_user(username='user1', password='password')
        )
        user_can_view.user_permissions.add(view_perm)
    
    def test_authentication(self):
        
        response = self.client.get(reverse('base:index'))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(reverse('base:index'), follow=True)
        
        html = response.content
        parser = self.parser(html)
        
        title = parser.css_first('title').text(strip=True)
        
        self.assertEqual(title, 'Login')
        
        self.client.login(user='user', password='password')
        response = self.client.get(reverse('base:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        
    def test_authorization(self):
        
        self.client.login(username='user1', password='password')
        
        response = self.client.get(reverse('faculties:index'))
        
        self.assertEqual(response.status_code, 200)
        
        parser = self.parser(response.content)
        title = parser.css_first('title').text(strip=True)
        
        self.assertEqual(title, 'Faculties')
        
        self.client.logout()
        
        self.client.login(username='user', password='password')
        
        response = self.client.get(reverse('faculties:index'))
        
        self.assertEqual(response.status_code, 403)
        parser = self.parser(response.content)
        title = parser.css_first('title').text(strip=True)
        
        self.assertEqual('Access Denied', title)
        
    def test_delete_one(self):
        
        qs = Faculty.objects.all().count()
        
        self.assertEqual(qs, 4)
        
        self.client.login(
            username='user',
            password='password',
        )
        
        response = self.client.post(
            reverse('faculties:delete', kwargs={'slug': 'dent'})
        )
        
        self.assertEqual(response.status_code, 200)
        
        qs = Faculty.objects.all().count()
        self.assertEqual(qs, 3)
        