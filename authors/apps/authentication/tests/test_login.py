"""user login tests"""
from .test_base import BaseTest
from rest_framework.views import status
from .test_data import (valid_user, valid_login,
                        wrong_password, wrong_email, missing_password_data, missing_email_data)


class UserLoginTest(BaseTest):
    """Contains user login test methods."""
    def test_user_can_login(self):
        """Tests if a user with valid credentials can login."""
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.post(self.login_url, valid_login, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_password_auth_fail(self):
        """Tests if a user with a wrong password cannot login."""
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.post(
            self.login_url, wrong_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['error'][0],
                         "A user with this email and password was not found.")

    def test_wrong_email(self):
        """Tests if a user with a wrong email cannot login."""
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.post(self.login_url, wrong_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['error'][0],
                         "A user with this email and password was not found.")

    def test_missing_password_value(self):
        """Tests if a user cannot login when no password is supplied."""
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.post(
            self.login_url, missing_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']
                         ['password'][0], "This field is required.")

    def test_missing_email_value(self):
        """Tests if a user cannot login when no email is supplied."""
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.post(
            self.login_url, missing_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']
                         ['email'][0], "This field is required.")
