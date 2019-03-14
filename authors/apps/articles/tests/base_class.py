from rest_framework.reverse import reverse
from authors.apps.authentication.tests import test_base
from .test_data import valid_article, valid_article_with_tags
from ..models import Article


class ArticlesBaseTest(test_base.BaseTest):
    def setUp(self):
        super().setUp()
        self.articles_url = reverse('articles:articles')

    def add_article(self):
        self.register_and_login_user()
        response = self.client.post(self.articles_url,
                                    data=valid_article,
                                    format='json')
        self.client.post(self.articles_url,
                         data=valid_article,
                         format='json')

    def add_tagged_article(self):
        self.register_and_login_user()
        self.client.post(self.articles_url,
                         data=valid_article_with_tags,
                         format='json')

    def like_article(self):
        article = Article.objects.all().first()
        return self.client.post(
            reverse(
                'articles:article-like',
                kwargs={
                    "slug": article.slug
                }
            ),
            format='json'
        )
