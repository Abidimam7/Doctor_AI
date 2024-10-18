# diagnosis/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class DiagnosisTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='patient', password='password', role='patient')
        self.doctor = get_user_model().objects.create_user(username='doctor', password='password', role='doctor')

    def test_patient_can_access_history(self):
        self.client.login(username='patient', password='password')
        response = self.client.get(reverse('patient_history'))
        self.assertEqual(response.status_code, 200)

    def test_doctor_can_access_dashboard(self):
        self.client.login(username='doctor', password='password')
        response = self.client.get(reverse('doctor_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_patient_cannot_access_doctor_dashboard(self):
        self.client.login(username='patient', password='password')
        response = self.client.get(reverse('doctor_dashboard'))
        self.assertEqual(response.status_code, 403)  # Forbidden for patients
