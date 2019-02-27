"""Contains tests for the profile operations"""

from rest_framework import status

from authors.apps.profile.models import Profile
import json
from authors.apps.profile.tests.test_base import BaseTest
from authors.apps.profile.tests.testdata import (user_profile,no_user_name_profile, user_profile2, valid_profile_update_data,user,user2,new_bio,no_avator_update_data)


class TestProfile(BaseTest):

    def test_can_get_user_profile(self):
        self.authenticate_test_user1()
        Profile.objects.create(user_profile)
        response = self.client.get(
            self.user_profile_url,
            content_type='application/json'
        )
        self.assertEqual(user_profile, response.data["profile"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_get_innexistent_user_profile(self):
        response = self.client.get(
            self.user_profile_url,
            content_type='application/json'
        )
        self.assertEqual("not found",
                         response.data["detail"])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_can_update_bio(self):
        response = self.client.put(self.user_update_profile_url,
                                   data=json.dumps(new_bio),
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile"]["bio"], new_bio["bio"])

    def test_can_update_profile(self):
        response = self.client.put(self.user_update_profile_url,
                                   data=user_profile,
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile"]["username"],
                         valid_profile_update_data["username"])
        self.assertEqual(response.data["profile"]["bio"],
                         valid_profile_update_data["bio"])

    def test_cannot_update_bio_not_logged_in(self):
        response = self.client.put(self.url,
                                   data=json.dumps(new_bio),
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_profile_with_no_username(self):
        response = self.client.put(self.url,
                                   data=json.dumps(no_user_name_profile),
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_update_profile_with_no_avator(self):
        response = self.client.put(self.url,
                                   data=json.dumps(no_avator_update_data),
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_update_profile_with_no_username_and_avater(self):
        response = self.client.put(self.url,
                                   data=json.dumps(no_avator_update_data),
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data["errors"]["image"])
