from django.test import TestCase
from .utils import parse_decimals


class BaseTest(TestCase):
    
    def test_parse_decimals(self):
        s1 = '12.14'
        s2 = '123,144,123.14'
        s3 = '123,144,123'
        self.assertEqual(12.14, parse_decimals(s1))
        self.assertEqual(123_144_123.14, parse_decimals(s2))
        self.assertEqual(123_144_123, parse_decimals(s3))