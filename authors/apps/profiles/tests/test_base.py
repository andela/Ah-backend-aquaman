"""Contains profile operations shared functioonality """

from authors.apps.profile.models import Profile
import json
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from authors.apps.profile.tests.testdata import (user_profile, user, user_profile2, user2)


class BaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_profile_url = reverse('profiles:profile')
        self.register_url = reverse('authentication:register')
        self.user_update_profile_url=reverse('profiles:update-profile')
        self.token=self.authenticate_test_user1()

    def authenticate_test_user1(self):
        response = self.client.post(self.register_url, data=json.dumps(
            user), content_type='application/json')
        res=self.client.force_login(user=response['user'])
        return res.data['token']

    def authenticate_test_user2(self):
        response = self.client.post(self.register_url, data=json.dumps(
            user2), content_type='application/json')
        self.client.force_login(user=response['user'])
