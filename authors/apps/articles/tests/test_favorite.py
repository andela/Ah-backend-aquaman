"""
test module for rating an article
"""
from django.urls import reverse
from authors.apps.articles.tests.base_class import ArticlesBaseTest
from ..models import Article


class TestRatingArticle(ArticlesBaseTest):
    """
    test class to contain functions to test rating an article
    """

    def setUp(self):
        super().setUp()

    def test_favorite_your_own_article(self):
        """
        method to test favorating your own article
        """
        self.add_article()
        article = Article.objects.all().first()
        response = self.client.post(
            reverse("articles:article-favorite", kwargs={'slug': article.slug})
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("article", response.json())

    def test_rate_someones_article(self):
        """
        method to test favorating someone's article
        """
        self.add_article()
        article = Article.objects.all().first()
        self.register_and_login_new_user()
        response = self.client.post(
            reverse("articles:article-favorite", kwargs={'slug': article.slug})
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("article", response.json())

    def test_favorite_non_existant_article(self):
        """
        method to test favorite non existant article
        """
        self.add_article()
        self.register_and_login_new_user()
        response = self.client.post(
            reverse("articles:article-favorite", kwargs={'slug': "play-chess"})
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("article", response.json())

    def test_unfavorite_an_article(self):
        """
        method to test unfavorating an article
        """
        self.add_article()
        article = Article.objects.all().first()
        self.register_and_login_new_user()
        self.client.post(
            reverse("articles:article-favorite", kwargs={'slug': article.slug})
        )
        response = self.client.delete(
            reverse("articles:article-favorite", kwargs={'slug': article.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("article", response.json())

    def test_unfavorite_article_not_in_your_favorites(self):
        """
        method to test unfavorating an article not in your favorites
        """
        self.add_article()
        article = Article.objects.all().first()
        self.register_and_login_new_user()
        response = self.client.delete(
            reverse("articles:article-favorite", kwargs={'slug': article.slug})
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("article", response.json())
