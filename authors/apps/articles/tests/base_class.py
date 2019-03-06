from rest_framework.reverse import reverse
from authors.apps.authentication.tests import test_base
from .test_data import valid_article


class ArticlesBaseTest(test_base.BaseTest):
    def setUp(self):
        super().setUp()
        self.articles_url = reverse('articles:articles')

    def add_article(self):
        self.register_and_login_user()
        self.client.post(self.articles_url,
                                    data=valid_article,
                                    format='json')
