"""
Test notifications app
"""
from django.urls import reverse
from rest_framework import status
from authors.apps.notifications.tests.test_base import BaseTestCase
from authors.apps.notifications.models import Notifications
from authors.apps.notifications.tests.test_data import (new_user, new_user_name)


class NotificationsTest(BaseTestCase):
    """
    Tests for notifications
    """

    def setUp(self):
        self.useraccess()

    def test_endpoint_for_notification(self):
        url = reverse('notification')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('notifications', response.json())

    def test_if_notification_created(self):
        self.create_notifications(new_user_name)
        notification = Notifications.objects.get(user_name='Apple')
        number_of_notifications = Notifications.objects.count()
        self.assertGreaterEqual(number_of_notifications, 1)

    def test_get_single_notification(self):
        url = reverse(
            'single_notification',
            kwargs={'pk': self.create_notifications(new_user_name)})
        response = self.client.get(url, format='json')
        self.assertFalse(response.data['status'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notification_that_does_not_exist(self):
        url = reverse('single_notification', kwargs={'pk': '10'})
        response = self.client.get(url, format='json')
        self.assertIn('notifications', response.json())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_notification_update(self):
        url = reverse(
            'single_notification',
            kwargs={'pk': self.create_notifications(new_user_name)})
        response = self.client.put(url, format='json')
        self.assertTrue(response.data['status'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
