from ..models import Article
from .base_class import ArticlesBaseTest
from ...profiles.models import Profile


class TestArticleModel(ArticlesBaseTest):
    """Tests class tests the article models __str__ method
    """

    def test_article_representation(self):
        """Tests returned data of model instance"""
        article = self.create_article()
        self.assertEqual(str(article), 'This is the title')

    def create_article(self):
        """Creates an article"""
        self.register_and_login_user()
        article = Article.objects.create(
            title='This is the title',
            description='This is the description',
            body='This is the body',
            author=Profile.objects.first())
        return article
