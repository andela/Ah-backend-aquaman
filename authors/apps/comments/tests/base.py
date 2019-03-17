from django.urls import reverse
from rest_framework.test import APITestCase
from ..tests.test_data import (new_user, user_login,
                            post_article, new_user2,
                            user_login2
                            )
from authors.apps.articles.models import Article


class BaseTestCase(APITestCase):
    """Has test helper methods."""

    def add_credentials(self, response):
        """adds authentication credentials in the request header"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response)

    def register_user(self, user_data):
        """register new user"""
        url = reverse('authentication:registration')
        return self.client.post(url, user_data, format='json')

    def verify_user(self, user_data):
        response = self.register_user(user_data)
        data = response.data
        verify_url = reverse('authentication:verify_email')
        res = self.client.get(verify_url+"?token=" + data["token"])
        return res

    def login_user(self, user_data):
        """login existing user"""
        url = reverse('authentication:login')
        return self.client.post(url, user_data, format='json')

    def user_access(self):
        """signup and login user"""
        self.verify_user(new_user)
        response = self.login_user(user_login)
        data = response.data
        self.add_credentials(data["token"])

    def user_access2(self):
        """signup and login user"""
        self.verify_user(new_user2)
        response = self.login_user(user_login2)
        data = response.data
        self.add_credentials(data["token"])

    def posting_article(self, post_data):
        url = reverse("articles:articles")
        return self.client.post(url, data=post_data, format='json')

    def article_slug(self):
        self.authorize_user_reg()
        self.posting_article(post_article)
        article = Article.objects.all().first()
        return article.slug

    def authorize_user_reg(self):
        res = self.login_user(user_login)
        self.add_credentials(res.data["token"])
