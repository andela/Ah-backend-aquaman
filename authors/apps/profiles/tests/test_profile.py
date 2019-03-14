"""
Test profiles app
"""
from django.urls import reverse

from authors.apps.profiles.tests.test_base import BaseTestCase

from .test_data import (new_user, update_profile)


class TestProfile(BaseTestCase):
    """Handles tests for the user profile feature/app"""

    def test_get_user_profile(self):
        """This test checks to see that a specific profile can be retrived"""
        self.register_user(new_user)
        url = reverse('profiles:get_profile', kwargs={'username': 'testuser12'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_non_existant_profile(self):
        """Tests for a non existant profile"""
        url = reverse('profiles:get_profile', kwargs={'username': 'testuser12'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 400)

    def test_update_user_profile(self):
        """Tests updating user profile"""
        self.authorize_user()
        url = reverse('profiles:update_profile', kwargs={'username': 'testuser12'})
        response = self.client.put(url, update_profile, format='json')
        self.assertEqual(response.status_code, 200)

    def test_list_all_users_profiles(self):
        """Tests retriving all profiles"""
        self.authorize_user()
        url = reverse('profiles:users_profiles')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_incorrect_user_update_profile(self):
        """Test user trying to update another users profile"""
        self.create_user()
        url = reverse('profiles:update_profile', kwargs={'username': 'testuser12'})
        response = self.client.put(url, update_profile, format='json')
        self.assertEquals(response.status_code, 403)

    def test_authorized_get_authors_list(self):
        """Test an authorised user getting authors list showing profiles of existing authors """
        self.authorize_user()
        url = reverse('profiles:authors_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_unauthorized_get_authors_list(self):
        """Test an unauthorised user getting authors list showing profiles of existing authors """
        url = reverse('profiles:authors_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_authorized_user_using_wrong_request_method_to_get_authors_list(self):
        """Test authorized user getting authors list using wrong request method"""
        self.authorize_user()
        url = reverse('profiles:authors_list')
        response = self.client.post(url)
        self.assertEquals(response.status_code, 405)

    def test_unauthorized_user_using_wrong_request_method_to_get_authors_list(self):
        """Test unauthorized user getting authors list using wrong request method"""
        url = reverse('profiles:authors_list')
        response = self.client.post(url)
        self.assertEquals(response.status_code, 403)

    def test_correct_authors_list_data_is_returned(self):
        """Test the correct data that is returned in the authors list"""
        self.authorize_user()
        url = reverse('profiles:authors_list')
        response = self.client.get(url)
        self.assertEquals(response.data[0]['email'], 'testuser@gmail.com')
        self.assertEquals(response.data[0]['username'], 'testuser12')
        self.assertIn('email', response.data[0]['profile'])
        self.assertIn('username', response.data[0]['profile'])
        self.assertIn('image', response.data[0]['profile'])
        self.assertIn('bio', response.data[0]['profile'])
        self.assertEquals(response.status_code, 200)
