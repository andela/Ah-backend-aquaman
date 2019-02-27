"""
Test articles app
"""
from django.urls import reverse

from rest_framework import status

from authors.apps.articles.tests.base import BaseTestCase

from .data import (article_missing_data, post_article,
                   update_article)


class TestArticle(BaseTestCase):
    """
    test class to contain functions to handle test for the article
    """

    def test_post_new_article(self):
        self.authorize_user()
        response = self.posting_article(post_article)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('articles', response.json())
        self.assertIsInstance(response.json().get("articles"), dict)

    def test_post_article_with_missing_data(self):
        self.authorize_user()
        url = reverse('articles')
        response = self.client.post(
            url, data=article_missing_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.json())

    def test_no_articles(self):
        self.authorize_user()
        url = reverse('articles')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('articles', response.json())
        self.assertIn(response.data['detail'],
                      'No articles found after search')

    def test_get_all_articles(self):
        self.authorize_user()
        url = reverse('articles')
        count = 0
        while count < 3:
            self.posting_article(post_article)
            count += 1
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_article_with_stats_succeeds(self):
        article = self.create_test_article_with_user()

        self.authorize_user()
        url = reverse(
            "get_update_destroy_article", kwargs=dict(slug=article.slug))
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_article(self):
        slug = self.slugger2()
        response = self.client.get(
            reverse("get_update_destroy_article", kwargs=dict(slug=slug)),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('articles', response.json())
        self.assertIsInstance(response.json().get("articles"), dict)

    def test_get_article(self):
        self.authorize_user()
        url = reverse('articles')
        self.posting_article(post_article)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("articles", response.json())
        self.assertIsInstance(response.json().get("articles"), dict)

    def test_update_article(self):
        self.authorize_user()
        url = reverse('articles')
        self.posting_article(post_article)
        response = self.client.get(url, format='json')
        data = response.json().get("articles")
        slug = data["results"][0]["slug"]
        response = self.client.put(
            reverse("get_update_destroy_article", kwargs=dict(slug=slug)),
            data=update_article,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('articles', response.json())
        self.assertIsInstance(response.json().get("articles"), dict)

    def test_delete_specific_article(self):
        self.authorize_user()
        url = reverse('articles')
        self.posting_article(post_article)
        response = self.client.get(url, format='json')
        data = response.json().get("articles")
        slug = data["results"][0]["slug"]
        response = self.deleter(slug)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('detail', response.data)
        self.assertIsInstance(response.data.get("detail"), str)
