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
        self.articles_url = reverse('articles:articles')

    def test_rate_your_own_article(self):
        """
        method to test rating your own article
        """
        self.add_article()
        article = Article.objects.all().first()
        response = self.client.post(
            reverse("articles:rating", kwargs={'slug': article.slug}),
            data={"article": {"score": 3}},
            format="json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("article", response.json())

    def test_rate_someones_article(self):
        """
        method to test rating someone's article
        """
        self.add_article()
        article = Article.objects.all().first()
        self.register_and_login_new_user()
        response = self.client.post(
            reverse("articles:rating", kwargs={'slug': article.slug}),
            data={"article": {"score": 3}},
            format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("article", response.json())

    def test_rate_out_of_range(self):
        """
        method to test rating an article using out of range values
        """
        self.add_article()
        article = Article.objects.all().first()
        self.register_and_login_new_user()
        response = self.client.post(
            reverse("articles:rating", kwargs={'slug': article.slug}),
            data={"article": {"score": 6}},
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("article", response.json())

    def test_rate_article_not_found(self):
        """
        method to test rating an article that does not exist
        """
        self.add_article()
        self.register_and_login_new_user()
        response = self.client.post(
            reverse("articles:rating", kwargs={'slug': "tommy"}),
            data={"article": {"score": 3}},
            format="json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("article", response.json())

    def test_rate_article_already_rated(self):
        """
        method to test rating an article already rated
        """
        "First Rating"
        self.add_article()
        article = Article.objects.all().first()
        self.register_and_login_new_user()
        self.client.post(
            reverse("articles:rating", kwargs={'slug': article.slug}),
            data={"article": {"score": 3}},
            format="json"
        )
        "Second rating"
        response = self.client.post(
            reverse("articles:rating", kwargs={'slug': article.slug}),
            data={"article": {"score": 3}},
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("article", response.json())
