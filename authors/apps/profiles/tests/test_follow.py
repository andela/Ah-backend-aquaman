from rest_framework import status
from django.urls import reverse
from .test_data import new_user, new_user_2
from authors.apps.profiles.tests.test_base import BaseTestCase


class FollowUsersTests(BaseTestCase):
    def test_user_can_follow_another_user(self):
        self.authorize_user_2()
        self.authorize_user()
        url = reverse('profiles:follow_user', kwargs={
                      'username': new_user_2['username']})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Successfuly followed', response.data['message'])

    def test_user_cannot_follow_a_user_that_doesnt_exist(self):
        self.authorize_user()
        url = reverse('profiles:follow_user', kwargs={'username': 'joel'})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Not found.', str(response.data))

    def test_user_cannot_double_follow_user(self):
        self.authorize_user_2()
        self.authorize_user()
        url = reverse('profiles:follow_user', kwargs={
                      'username': new_user_2['username']})
        self.client.post(url, format='json')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You are already following ' +
                      str(new_user_2['username']), str(response.data))

    def test_user_cannot_follow_self(self):
        self.authorize_user()
        url = reverse('profiles:follow_user', kwargs={
                      'username': new_user['username']})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You cannot follow your own profile.', str(response.data))

    def test_user_can_unfollow_another_user(self):
        self.authorize_user_2()
        self.authorize_user()
        url = reverse('profiles:follow_user', kwargs={
                      'username': new_user_2['username']})
        self.client.post(url, format='json')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('You have successfully unfollowed ' +
                      str(new_user_2['username']), str(response.data))

    def test_user_cannot_unfollow_a_user_they_are_not_following(self):
        self.authorize_user_2()
        self.authorize_user()
        url = reverse('profiles:follow_user', kwargs={
                      'username': new_user_2['username']})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You cannot unfollow a user you are not following.', str(response.data))

    def test_user_cannot_unfollow_a_user_that_doesnt_exist(self):
        self.authorize_user()
        url = reverse('profiles:follow_user', kwargs={'username': 'joel'})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Not found.', str(response.data))

    def test_return_list_of_followings_for_a_user(self):
        self.authorize_user_2()
        self.authorize_user()
        url = reverse(
            'profiles:follow_user', kwargs={'username': new_user_2['username']})
        get_url = reverse(
            'profiles:follow_user', kwargs={'username': new_user['username']})
        self.client.post(url, format='json')
        response = self.client.get(get_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('following', str(response.data))
        self.assertEqual(response.data['following_count'], 1)
        self.assertIn('followed_at', str(response.data))

    def test_return_followings_of_a_user_that_doesnt_exist(self):
        self.authorize_user()
        url = reverse('profiles:follow_user', kwargs={'username': 'joel'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Not found.', str(response.data))

    def test_return_followers_for_a_user_that_doesnt_exist(self):
        self.authorize_user()
        url = reverse('profiles:get_followers', kwargs={'username': 'joel'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Not found.', str(response.data))

    def test_user_with_no_followers(self):
        self.authorize_user_2()
        self.authorize_user()
        url = reverse(
            'profiles:get_followers', kwargs={'username': new_user_2['username']})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('has no followers', str(response.data))

    def test_return_followers_of_a_user(self):
        self.authorize_user_2()
        self.authorize_user()
        url = reverse('profiles:get_followers', kwargs={
                      'username': new_user_2['username']})
        get_url = reverse('profiles:get_followers', kwargs={
                          'username': new_user_2['username']})
        self.client.post(url, format='json')
        response = self.client.get(get_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('has no followers', response.data['message'])
