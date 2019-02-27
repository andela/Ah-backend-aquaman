from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

class UserLoginTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login = reverse('authentication:login')
        self.registration = reverse('authentication:registration')

        self.valid_user = {
            "user": {
                "username": "Bagzie",
                "email": "bagendadeogracious@gmail.com",
                "password": "Password123"
            }
        }

        self.valid_login = {
            "user": {
                "email": "bagendadeogracious@gmail.com",
                "password": "Password123"
            }
        }

        self.wrong_password = {
            "user": {
                "email": "bagendadeogracious@gmail.com",
                "password": "Password12"
            }
        }

        self.wrong_email = {
            "user": {
                "email": "bagenda@gmail.com",
                "password": "Password123"
            }
        }

        self.missing_password_key = {
            "user": {
                "email": "Password123"
            }
        }

    def test_valid_login(self):
        self.client.post(self.registration, self.valid_user, format='json')
        response = self.client.post(self.login, self.valid_login, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_wrong_password(self):
        self.client.post(self.registration, self.valid_user, format='json')
        response = self.client.post(self.login, self.wrong_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['error'][0], "A user with this email and password was not found.")

    def test_wrong_email(self):
        self.client.post(self.registration, self.valid_user, format='json')
        response = self.client.post(self.login, self.wrong_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['error'][0], "A user with this email and password was not found.")

    def test_missing_password_key(self):
        self.client.post(self.registration, self.valid_user, format='json')
        response = self.client.post(self.login, self.missing_password_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['password'][0], "This field is required.")
