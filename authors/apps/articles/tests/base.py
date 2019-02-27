"""
    this file sets the common features to be used by
    our testcase file
"""
from django.urls import reverse
from rest_framework.test import APITestCase
from .data import (new_user, post_article,
                   post_article_2, article_missing_data)
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article


class BaseTestCase(APITestCase):

    def add_credentials(self, response):
        """ adds authentication credentials in the request header """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response)

    def register_user(self, user_data):
        """register new user"""
        url = reverse('authentication')
        return self.client.post(url, user_data, format='json')

    def authorize_user(self):
        res = self.register_user(new_user)
        self.add_credentials(res.data["token"])

    def posting_article(self, post_data):
        url = reverse("articles")
        return self.client.post(url, data=post_data, format='json')

    def delete_article(self, slug):
        return self.client.delete(
            reverse("get_update_destroy_article", kwargs=dict(slug=slug)),
            format='json')

    def favourate_article(self, slug):
        return self.client.put(
            reverse("favourite", kwargs=dict(slug=slug)), format="json")

    def unfavourate_article(self, slug):
        return self.client.delete(
            reverse("undo_favourite", kwargs=dict(slug=slug)), format="json")
