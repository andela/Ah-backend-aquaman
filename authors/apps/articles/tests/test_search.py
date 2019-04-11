from django.urls import reverse

from rest_framework import status

from authors.apps.articles.tests.base_class import ArticlesBaseTest
from .test_data import valid_article
from ..models import Article


class TestSearchArticle(ArticlesBaseTest):

    def test_search_by_keyword(self):
        """
        Tests if a user can search articles by keyword
        """
        self.add_article()
        response = self.client.get(self.articles_url+"?keyword=the")
        self.assertIn("the", response.data['articles'][0]['description'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_tag(self):
        """
        Tests if a user can search articles by tag
        """
        self.add_tagged_article()
        response = self.client.get(self.articles_url+"?tag=apps")
        self.assertIn("apps", response.data['articles'][0]['tagList'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_author(self):
        """
        Tests if a user can search articles by an author
        """
        self.add_tagged_article()
        response = self.client.get(self.articles_url+"?author=Bagzie12")
        self.assertIn("Bagzie12", response.data['articles'][0]['author']['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
