from django.urls import reverse
from rest_framework.test import APITestCase
from .test_data import new_user, new_user_2


class BaseTestCase(APITestCase):

    def add_credentials(self, response):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response)

    def register_user(self, user_data):
        url = reverse('authentication:registration')
        return self.client.post(url, user_data, format='json')

    def authorize_user(self):
        url = reverse('authentication:verify_email')
        response = self.register_user(new_user)
        data = response.json().get("user")
        self.client.get(url + "?token=" + data['token'], format='json')
        self.add_credentials(data["token"])

    def authorize_user_2(self):
        url = reverse('authentication:verify_email')
        response = self.register_user(new_user_2)
        data = response.json().get("user")
        self.client.get(url + "?token=" + data['token'], format='json')
        self.add_credentials(data["token"])

    def create_user(self):
        url = reverse('authentication:registration')
        self.client.post(url, new_user, format='json')
