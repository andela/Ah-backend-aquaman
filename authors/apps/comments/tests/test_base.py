"""Contains comment operations shared functioonality """


from authors.apps.articles.models import Article
from authors.apps.profiles.models import Profile
from authors.apps.comments.models import Comment
import json
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from authors.apps.comments.tests.test_data import (comment, comment_no_body,
                                                   user,user2, article_response,
                                                   article, single_reply)


class BaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.add_comment_url = reverse('comments:add-comment')
        self.delete_comment_url = reverse('comments:delete-comment')
        self.update_comment_url = reverse('comments:update-comment')
        self.all_comments_url = reverse('comments:all-comments')
        self.single_comment_url = reverse('comments:single-comment')
        self.comment_reply_url = reverse('comments:comment-reply')
        self.register_url = reverse('authentication:register')
        self.dislike_comment_url=reverse('comments:dislike-comment')
        self.like_comment_url=reverse('comments:like_comment')

    def create_article(self):
        Article.objects.create(
            article)
        self.article = Article.objects.all().first()
        self.slug = self.article.slug
        self.comment_url = reverse(
            'comments:comment', kwargs={'slug': self.slug})

    def add_comment(self,user,article):
        comment = Comment(body="New Comment", article=article,author=Profile.objects.get(user=user))
        comment.save()
        return comment

    def reply_to_comment(self):
        self.reply = self.client.post(
            self.comment_reply_url,
            data=json.dumps(single_reply),
            content_type='application/json'
        )
        self.reply_id = self.reply.data["reply"]["id"]



    def create_and_login_user(self):
        response = self.client.post(self.register_url, data=json.dumps(
            user), content_type='application/json')
        self.client.force_login(user=response['user'])


    def authenticate_test_user(self):
        response = self.client.post(self.register_url, data=json.dumps(
            user2), content_type='application/json')
        self.client.force_login(user=response['user'])
