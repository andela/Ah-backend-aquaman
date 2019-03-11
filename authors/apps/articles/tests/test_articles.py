from django.urls import reverse

from rest_framework import status

from authors.apps.articles.tests.base_class import ArticlesBaseTest
from .test_data import valid_article
from ..models import Article


class TestArticle(ArticlesBaseTest):
    def test_create_article(self):
        """
        Tests method tests wether a user can create anew article
        """
        self.register_and_login_user()
        response = self.client.post(self.articles_url,
                                    data=valid_article,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_article_if_user_is_not_authenticated(self):
        """
        Tests a user that is not authenticated cannot
        create an article.
        message
        """
        response = self.client.post(self.articles_url,
                                    data=valid_article,
                                    format='json')
        expected_dict = {
            "detail": "Authentication credentials were not provided."
        }
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(expected_dict, response.data)

    def test_retrieve_get_articles_if_there_is_no_article_in_db(self):
        """
       Tests wether an empty list is returned no one has created an article
        """
        response = self.client.get(self.articles_url)
        self.assertEqual({'articles': [], 'articleCount': 0}, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_all_articles(self):
        """
        Tests if a user can get articles after adding an article
        """
        self.add_article()
        response = self.client.get(self.articles_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_article(self):
        """Tests if a user can view a single article"""
        self.add_article()
        article = Article.objects.all().first()
        response = self.client.get(reverse('articles:article-detail',
                                           kwargs={'slug': article.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.data)

    def test_get_un_existing_slug(self):
        """Tests if an article cannot be returned if true"""
        response = self.client.get(reverse('articles:article-detail',
                                           kwargs={'slug':
                                                   'testdfd'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        expected_dict = {
            'errors': 'that article was not found'}
        self.assertEqual(expected_dict, response.data)

    def test_edit_when_logged_in(self):
        """Tests if a user is prohibited to edit when not logged in"""
        self.add_article()
        article = Article.objects.all().first()
        response = self.client.patch(
            reverse('articles:article-detail',
                    kwargs={'slug': article.slug}),
            data=valid_article,
            format='json')
        
        self.assertIn('title', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_an_article_not_permitted(self):
        """Tests if a user cannot edit an article he didnot author"""
        self.add_article()
        self.register_and_login_new_user()
        article = Article.objects.all().first()
        response = self.client.patch(
            reverse('articles:article-detail',
                    kwargs={'slug': article.slug}),
            data=valid_article,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_innexistent_article_slug(self):
        """Tests if a user cant updated an innexistent article"""
        self.register_and_login_user()
        response = self.client.patch(
            reverse('articles:article-detail',
                    kwargs={'slug': 'slugish'}),
            data=valid_article,
            format='json')
        expected_dict = {
            'errors': 'that article was not found'}
        self.assertDictEqual(expected_dict, response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_an_article_logged_in(self):
        """Tests if an artical cannot be deleted when unauthenticated"""
        self.add_article()
        article = Article.objects.first()
        response = self.client.delete(reverse('articles:article-detail',
                                              kwargs={'slug': article.slug}),
                                      format='json')
        expected_dict = {'article': 'Article has been deleted'}
        self.assertDictEqual(expected_dict, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_an_article_not_permitted(self):
        """Tests if a user cannor delete an article they didnot author"""
        self.add_article()
        self.register_and_login_new_user()
        article = Article.objects.first()
        response = self.client.delete(reverse('articles:article-detail',
                                              kwargs={'slug': article.slug}),
                                      format='json')
        expected = {
            'detail': 'You do not have permission to perform this action.'}
        self.assertDictEqual(expected, response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_innexistent_article(self):
        """Tests if a user cannot delete an article that doesnot exist"""
        self.add_article()
        response = self.client.delete(reverse(
            'articles:article-detail',
            kwargs={'slug':
                    'sheshowsup'}),
            data=valid_article,
            format='json')
        expected_dict = {
            'errors': 'that article was not found'}
        self.assertDictEqual(expected_dict, response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successful_article_like(self):
        """Tests if a user can like an article successfully."""
        self.add_article()
        article = Article.objects.all().first()
        response = self.like_article()
        self.assertEqual(response.data['details']['likes'], True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successful_article_dislike(self):
        """Tests if a user can like an article successfully."""
        self.add_article()
        self.like_article()
        response = self.like_article()
        self.assertEqual(response.data['details']['likes'], False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
