from django.urls import reverse
from authors.apps.articles.tests.base_class import ArticlesBaseTest
from ..models import Article


class TestReadStats(ArticlesBaseTest):
    """Read stats tests"""
    def setUp(self):
        super().setUp()

    def test_an_author_reading_their_own_article(self):
        """Test for an author reading their own article"""
        self.add_article()
        article = Article.objects.all().first()
        url = reverse("articles:article-detail", kwargs={'slug': article.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_an_author_reading_another_authors_article(self):
        """Test for an author reading another authors article"""
        self.add_article()
        self.register_and_login_new_user()
        article = Article.objects.all().first()
        url = reverse("articles:article-detail", kwargs={'slug': article.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_get_an_article_showing_their_reading_stats(self):
        """Test for an user getting an article showing the number of articles they have read and how many times
        they have read a particular article
        """
        self.add_article()
        self.register_and_login_new_user()
        article = Article.objects.all().first()
        self.client.get(reverse("articles:article-detail", kwargs={'slug': article.slug}))
        url = reverse("articles:reading-stats", kwargs={'slug': article.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_get_an_article_showing_their_reading_stats_using_wrong_slug(self):
        """Test for an user getting their reading stats using a wrong article slug"""
        self.add_article()
        self.register_and_login_new_user()
        article = Article.objects.all().first()
        self.client.get(reverse("articles:article-detail", kwargs={'slug': article.slug}))
        url = reverse("articles:reading-stats", kwargs={'slug': 'amwrong'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
