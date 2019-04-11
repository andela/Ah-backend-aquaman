from rest_framework import status


from authors.apps.articles.tests.base_class import ArticlesBaseTest
from .test_data import valid_article_with_tags
from django.urls import reverse
import time


class TestTags(ArticlesBaseTest):
    def test_create_article_with_tags(self):
        """
        Tests method tests wether a user can create anew article with tags
        """
        self.register_and_login_user()
        response = self.client.post(self.articles_url,
                                    data=valid_article_with_tags,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_article_with_tags(self):
        """Tests if one can get tags"""
        self.add_tagged_article()
        response = self.client.get(reverse('articles:article-tags'),
                                   format='json')
        self.assertEqual(type(response.data['tags']), set)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
