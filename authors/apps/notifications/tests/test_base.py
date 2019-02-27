from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from authors.apps.authentication.models import User
from authors.apps.notifications.models import Notifications
import json
from authors.apps.notifications.tests.test_data import (new_user, user_login, notifications)


class BaseTestCase(APITestCase):
    """
    Defines functions to handle notification tests
    """
    def add_credentials(self, response):
        """adds authentication credentials in the request header"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response)

    def register_user(self, user_data):
        """register new user"""
        url = reverse('authentication')
        return self.client.post(url, user_data, format='json')

    def verify_user(self, user_data):
        response = self.register_user(user_data)
        token = response.data['token']
        verify_url = "/api/users/verify?token={}".format(token)
        res = self.client.get(verify_url)
        return res

    def login_user(self, user_data):
        """login existing user"""
        url = reverse('login')
        return self.client.post(url, user_data, format='json')

    def useraccess(self):
        """signup and login user"""
        self.verify_user(new_user)
        response = self.login_user(user_login)
        self.add_credentials(response.data['token'])

    def create_notifications(self, username):
        user = User.objects.get(username=username)
        title = 'Create an article'
        body = 'Article has been created'
        notifications = Notifications(user=user, type=title, body=body)
        notifications.save()
        return notifications.id
