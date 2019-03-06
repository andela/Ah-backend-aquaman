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
