from django.urls import reverse
from authors.apps.articles.tests.base_class import ArticlesBaseTest
from ..models import Article


class TestBookmarks(ArticlesBaseTest):
    """Bookmark tests"""
    def setUp(self):
        super().setUp()

    def test_bookmark_your_own_article(self):
        """Test for bookmarking your own article an article"""
        self.add_article()
        article = Article.objects.all().first()
        url = reverse("articles:bookmark_article", kwargs={'slug': article.slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertIn(response.data['error'], 'You can not bookmark your own article')

    def test_bookmark_another_authors_article(self):
        """Test for bookmarking another authors article"""
        self.add_article()
        self.register_and_login_new_user()
        article = Article.objects.all().first()
        url = reverse("articles:bookmark_article", kwargs={'slug': article.slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertIn(response.data['message'], 'Article has been bookmarked')

    def test_bookmark_article_that_does_not_exist(self):
        """Test for bookmarking an article that does not exist"""
        self.add_article()
        self.register_and_login_new_user()
        url = reverse("articles:bookmark_article", kwargs={'slug': 't990'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertIn(response.data['detail'], 'Not found.')

    def test_bookmark_article_that_has_already_been_bookmarked(self):
        """Test bookmarking an article that has already been bookmarked"""
        self.add_article()
        self.register_and_login_new_user()
        article = Article.objects.all().first()
        self.client.post(reverse("articles:bookmark_article", kwargs={'slug': article.slug}))
        url = reverse("articles:bookmark_article", kwargs={'slug': article.slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertIn(response.data['error'], 'You have already bookmarked this article')

    def test_unbookmark_article(self):
        """Test for unbookmarking an article"""
        self.add_article()
        self.register_and_login_new_user()
        article = Article.objects.all().first()
        self.client.post(reverse("articles:bookmark_article", kwargs={'slug': article.slug}))
        url = reverse("articles:bookmark_article", kwargs={'slug': article.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.data['message'], 'Article has been unbookmarked')

    def test_unbookmark_article_that_has_already_been_unbookmarked(self):
        """Test for unbookmarking an article that has already been unbookmarked"""
        self.add_article()
        self.register_and_login_new_user()
        article = Article.objects.all().first()
        self.client.post(reverse("articles:bookmark_article", kwargs={'slug': article.slug}))
        self.client.delete(reverse("articles:bookmark_article", kwargs={'slug': article.slug}))
        url = reverse("articles:bookmark_article", kwargs={'slug': article.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)
        self.assertIn(response.data['error'], 'Article does not exist in your bookmarks list')

    def test_get_bookmarked_articles(self):
        """Test to get bookmarked articles by a user"""
        self.add_article()
        self.register_and_login_new_user()
        article = Article.objects.all().first()
        self.client.post(reverse("articles:bookmark_article", kwargs={'slug': article.slug}))
        url = reverse('articles:articles_bookmarked')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_no_articles_bookmarked(self):
        """Test to get empty bookmarks list"""
        self.add_article()
        self.register_and_login_new_user()
        url = reverse('articles:articles_bookmarked')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.data['message'], 'You have not bookmarked any articles yet')

    def test_unbookmark_article_that_does_not_exist(self):
        """Test unbookmark article that does not exist in the bookmarks list"""
        self.add_article()
        self.register_and_login_new_user()
        url = reverse("articles:bookmark_article", kwargs={'slug': 't990'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertIn(response.data['detail'], 'Not found.')
