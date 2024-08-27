from django.test import TestCase

from ..utils import dict_to_css, parse_decimals


class TestUtils(TestCase):
    
    def test_dict_to_css(self):
        styles = {
            'background': 'lime',
            'opacity': 0.5,
        }
        styles_str = dict_to_css(styles)
        self.assertEqual(
            'background: lime; opacity: 0.5;',
            styles_str
        )
        
    def test_parse_decimals(self):
        num1 = '12312,412,41231.121'
        num2 = '123.123.1212'
        num3 = '1231 312   3123 12 . 12 .12'
        num4 = '211asfdwfvv.131,1213'
        num5 = '12,000.12'
        num6 = '12,000'
        
        self.assertEqual(parse_decimals(num1), 1231241241231.121)
        self.assertEqual(parse_decimals(num2), 123.123)
        self.assertEqual(parse_decimals(num3), 1231312312312.12)
        self.assertEqual(parse_decimals(num4), 211.131)
        self.assertEqual(parse_decimals(num5), 12000.12)
        self.assertEqual(parse_decimals(num6), 12000)