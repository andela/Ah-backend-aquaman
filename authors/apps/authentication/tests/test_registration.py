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

        self.empty_username = {
            "user": {
                "username": "",
                "email": "bagendadeogracious@gmail.com",
                "password": "Password123"
            }
        }

        self.wrong_email = {
            "user": {
                "username": "Bagzie",
                "email": "bagendadegmail.com",
                "password": "Password123"
            }
        }

        self.short_password = {
            "user": {
                "username": "Bagzie",
                "email": "bagendadeogracious@gmail.com",
                "password": "Pass"
            }
        }

        self.missing_username_key = {
            "user": {
                "email": "bagendadeogracious@gmail.com",
                "password": "Password123"
            }
        }

    def test_valid_registration(self):
        response = self.client.post(self.registration, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], "Bagzie")

    def test_empty_username(self):
        response = self.client.post(self.registration, self.empty_username, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['username'][0], "This field may not be blank.")

    def test_wrong_email(self):
        response = self.client.post(self.registration, self.wrong_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['email'][0], "Enter a valid email address.")

    def test_short_pass(self):
        response = self.client.post(self.registration, self.short_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['password'][0], "Ensure this field has at least 8 characters.")

    def test_missing_username_key(self):
        response = self.client.post(self.registration, self.missing_username_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['username'][0], "This field is required.")

    def test_existing_email(self):
        self.client.post(self.registration, self.valid_user, format='json')
        response = self.client.post(self.registration, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['email'][0], "user with this email already exists.")
