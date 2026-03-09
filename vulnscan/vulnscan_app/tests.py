from django.test import TestCase
from django.urls import reverse
from .risk_level import classify_risk
from django.contrib.auth.models import User




class ScanPageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_scan_page_loads(self):
        response = self.client.get(reverse('start_scan'))
        self.assertEqual(response.status_code, 302)

class RisktTest(TestCase):

    def test_high_risk_port(self):
        self.assertEqual(classify_risk(21), "High") 
        
        
    def test_medium_risk_port(self):
        self.assertEqual(classify_risk(80), "Medium")


