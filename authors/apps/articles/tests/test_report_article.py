from rest_framework import status
from authors.apps.articles.tests.base_class import ArticlesBaseTest
from .test_data import valid_reported_article
from authors.apps.articles.models import Article
from django.urls import reverse


class TestReportArticle(ArticlesBaseTest):
    def test_can_not_report_own_article(self):
        """
        Tests method tests a user who is authenticated can report his/her own article
        """

        self.add_article()

        article = Article.objects.all().first()
        response = self.client.post(
            reverse('articles:report-article',
                    kwargs={'slug': article.slug}),
            data=valid_reported_article, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         'You cannot report your own article')

    def test_can_report_some_article(self):
        """
        Tests if a user who is authenticated can report some article
        """

        self.add_article()
        self.register_and_login_new_user()

        article = Article.objects.all().first()
        response = self.client.post(
            reverse('articles:report-article',
                    kwargs={'slug': article.slug}),
            data=valid_reported_article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_report_some_article_not_logged_in(self):
        """
        Tests if a user who is authenticated can report some article
        """
        self.add_article()
        article = Article.objects.all().first()
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(
            reverse('articles:report-article',
                    kwargs={'slug': article.slug}),
            data=valid_reported_article, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
