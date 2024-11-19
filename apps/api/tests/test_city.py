import json

from django.contrib.auth.models import User, Permission
from django.test import TestCase

from apps.cities.models import City


class CityTestCase(TestCase):
    def setUp(self):
        user_with_perms = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testuser",
        )
        view_cities = Permission.objects.get(codename="view_city")
        user_with_perms.user_permissions.add(view_cities)
        User.objects.create_user(
            username="testuser2",
            email="testuser2@test.com",
            password="testuser2",
        )
        logged_in: bool = self.client.login(
            username="testuser", password="testuser"
        )
        cities = [
            City(name="City 1", description="Description 1"),
            City(name="City 2", description="Description 2"),
            City(name="City 22", description="Description 22"),
            City(name="City 3", description="Description 3"),
        ]
        for city in cities:
            city.save()

    def test_filter_djangoql(self):
        response = self.client.get('/api/cities/?djangoql=name ~ "2"')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
        self.assertEqual(len(response.json()["results"]), 2)

        response_2 = self.client.get('/api/cities/?name=2')
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_2.json()["status"], 200)
        self.assertEqual(len(response_2.json()["results"]), 2)

        self.assertEqual(response.json()["results"], response_2.json()["results"])

    def test_authorization(self):
        self.client.logout()
        self.client.login(username="testuser2", password="testuser2")
        response = self.client.get("/api/cities/")

        self.assertEqual(response.status_code, 401)

    def test_get_list(self):
        response = self.client.get("/api/cities/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
        self.assertEqual(len(response.json()["results"]), 4)

    def test_get_list_with_pagination(self):
        response = self.client.get("/api/cities/?limit=1&offset=0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_get_list_with_filter(self):
        response = self.client.get("/api/cities/?name=City 2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
        self.assertEqual(len(response.json()["results"]), 2)

    def test_get_detail(self):
        response = self.client.get("/api/cities/city-1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
        self.assertEqual(response.json()["results"]["name"], "City 1")

    def test_create_object(self):
        for idx in range(4, 12):
            response = self.client.post(
                "/api/cities/",
                json.dumps(
                    {
                        "name": f"City {idx}",
                        "description": f"Description {idx}",
                    }
                ),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["status"], 201)
            self.assertEqual(response.json()["results"]["name"], f"City {idx}")
            self.assertEqual(response.json()["results"]["slug"], f"city-{idx}")

        cities_count = City.objects.all().count()

        self.assertEqual(cities_count, 12)
    
    def test_delete_object(self):
        response = self.client.delete("/api/cities/city-1")
        self.assertEqual(response.status_code, 204)
        cities_count = City.objects.all().count()
        self.assertEqual(cities_count, 3)

    def test_bulk_create(self):
        
        data = json.dumps(
            [
                {
                    "name": f"City {idx}",
                    "description": f"Description {idx}",
                }   
                for idx in range(4, 12)
            ]
        )

        response = self.client.post(
            "/api/cities/bulk/",
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], 201)

        cities_count = City.objects.all().count()

        self.assertEqual(cities_count, 12)
