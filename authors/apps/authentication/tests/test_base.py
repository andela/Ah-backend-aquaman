"""Base file containing setup"""


from rest_framework.test import APIClient, APITestCase
from django.urls import reverse


class BaseTest(APITestCase):
    """Contains test setup method."""

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:login')
        self.registration_url = reverse('authentication:registration')
