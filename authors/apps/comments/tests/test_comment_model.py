"""
Test comments model
"""
from django.urls import reverse
from rest_framework import status

from ..tests.test_data import (post_article, comment,
                                update_comment
                    )

from authors.apps.comments.tests.base import BaseTestCase
from ..models import Comment, CommentLike
from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article

class TestComment(BaseTestCase):
    """
    test class to contain functions to handle test for the commenting on an article
    """
    def setUp(self):
        super().setUp()
        self.verified_user = User.objects.create_user(
            username='testuser1',
            email='testemail1@test.com',
            password='testpassworD12')
        self.profile=Profile.objects.get(user=self.verified_user)
        self.created_article=Article.objects.create(
            body=' hello world',description='a description',
            title='a title',author=self.profile
        )
        self.testcomment=Comment.objects.create(body='a test comment body',
                            commented_by=self.profile,
                            article=self.created_article)


    def test_comment_str_return(self):
        """
        Test create comment 
        """
        self.comment = Comment.objects.create(
            body='A comment body', commented_by=self.profile, article=self.created_article)
        self.assertEqual(self.comment.__str__(), 'A comment body')

    def test_commentlike_str_return(self):
        """
        Test like a comment
        """
        self.commentLike = CommentLike.objects.create(
            liked_by=self.profile, comment=self.testcomment, like_status=True)
        self.assertEqual('testuser1', self.commentLike.__str__())
