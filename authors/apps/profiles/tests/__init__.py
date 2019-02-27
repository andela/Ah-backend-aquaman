from authors.apps.articles.models import Article
import json
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .test_data import comment, comment_no_body, user, article_response, article, single_reply


class BaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.add_comment_url = reverse('comments:add-comment')
        self.delete_comment_url = reverse('comments:delete-comment')
        self.update_comment_url = reverse('comments:update-comment')
        self.all_comments_url = reverse('comments:all-comments')
        self.single_comment_url = reverse('comments:single-comment')
        self.comment_reply_url = reverse('comments:comment-reply')

    def create_article(self):
        Article.objects.create(
            article)
        self.article = Article.objects.all().first()
        self.slug = self.article.slug
        self.comment_url = reverse(
            'comments:comment', kwargs={'slug': self.slug})

    def reply_to_comment(self):
        self.reply = self.client.post(
            self.comment_reply_url,
            data=json.dumps(single_reply),
            content_type='application/json'
        )
        self.reply_id = self.reply.data["reply"]["id"]

    def add_comment(self):
        self.create_and_login__user()
        self.comment = self.client.post(
            self.add_comment_url,
            data=json. dumps(comment),
            content_type='application/json'
        )
        self.comment_id = self.comment.data["comment"]["id"]
