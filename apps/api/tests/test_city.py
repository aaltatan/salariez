import json

from django.test import TestCase
from ninja.testing import TestClient

from apps.cities.models import City
from ..routers.city import router


class CityTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        cities = [
            City(name="City 1", description="Description 1"),
            City(name="City 2", description="Description 2"),
            City(name="City 22", description="Description 22"),
            City(name="City 3", description="Description 3"),
        ]
        for city in cities:
            city.save()

    def test_get_list(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
        self.assertEqual(len(response.json()["results"]), 4)

    def test_get_list_with_pagination(self):
        response = self.client.get("?limit=1&offset=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_get_list_with_filter(self):
        response = self.client.get("?name=City 2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
        self.assertEqual(len(response.json()["results"]), 2)

    def test_get_detail(self):
        response = self.client.get("/city-1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
        self.assertEqual(response.json()["results"]["name"], "City 1")

    def test_create_object(self):
        response = self.client.post(
            "",
            json.dumps(
                {
                    "name": "City 4",
                    "description": "Description 4",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], 201)
        self.assertEqual(response.json()["results"]["name"], "City 4")
        self.assertEqual(len(response.json()["results"]), 5)
        self.assertEqual(response.json()["results"]["slug"], "city-4")
