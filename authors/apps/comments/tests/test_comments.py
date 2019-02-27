"""Contains tests for the comment operations """

from django.urls import reverse

from rest_framework import status

from authors.apps.authentication.models import User
from authors.apps.comments.models import Comment
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article
import json
from .test_base import TestBase
from test_data import comment, single_comment_url, user


class TestComments(TestBase):

    def test_user_can_view_comments_on_article(self):
        self.authenticate_test_user()
        response = self.client.get(
            self.comments_url,
            content_type='application/json'
        )
        self.assertEqual([], response.data["comments"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_didnt_authenticate(self):
        response = self.client.post(
            self.comments_url,
            data=json.dumps(comment),
            content_type='application/json'
        )
        self.assertEqual("Authentication credentials were not provided.",
                         response.data["detail"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_add_comments(self):
        self.add_comment()
        self.assertEqual(self.comment.status_code, status.HTTP_201_CREATED)

    def test_user_can_get_all_comments(self):
        self.add_comment()
        response = self.client.get(
            self.comments_url, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_single_comment(self):
        self.add_comment()
        response = self.client.get(self.single_comment_url,
                                   content_type='application/json'
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_edit_comment_if_you_created_it(self):
        self.add_comment()
        response = self.client.patch(self.update_comment_url,
                                     data=json.dumps(comment),
                                     content_type='application/json'
                                     )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_edit_comment_if_you_didnt_author_it(self):
        self.add_comment()
        response = self.client.patch(self.update_comment_url,
                                     data=json.dumps(comment),
                                     content_type='application/json'
                                     )
        self.assertEqual(
            "Not allowed",
            response.data['response'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_comment(self):
        self.add_comment()
        response = self.client.patch(self.delete_comment_url,
                                     data=json.dumps(comment),
                                     content_type='application/json'
                                     )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_add_an_empty_comment(self):
        self.register_and_login_user()
        response = self.client.post(self.comments_url,
                                    data=comment_no_body,
                                    format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data['message'], "Could not create comment")
        self.assertEqual(str(response.data['errors']['commenting_on'][0]),
                         "You cannot comment on text not in the article")

    def test_edit_comments_with_no_body(self):
        self.add_comment()
        response = self.client.patch(self.comment_detail_url,
                                     data=comment_no_body,
                                     format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data['message'], "failed to edit comment")


    def test_cannot_get_likes_of_no_comment(self):
        self.add_comment()
        response = self.client.get(
            reverse(
                'comments:comment-likes', kwargs={'pk': self.comment_id + 1}),
            content_type='application/json'
        )
        self.assertIn(
            "not found",
            response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_cannot_like_nonexistent_comment(self):
        self.add_comment()
        response = self.client.post(
            reverse(
                'comments:comment-likes', kwargs={'pk': self.comment_id + 1}),
            content_type='application/json'
        )
        self.assertIn(
            "not found!",
            response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_can_like_own_comment(self):
        self.add_comment()
        response = self.client.post(
            self.like_comment_url,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_cannot_like_comment_more_than_once(self):
        self.add_comment()
        response = self.client.post(
            self.like_comment_url,
            content_type='application/json'
        )
        response = self.client.post(
            self.like_comment_url,
            content_type='application/json'
        )
        self.assertIn(
            "you already like this",
            response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_cannot_delete_like_comment_you_did_not_like(self):
        self.add_comment()
        self.authenticate_test_user()
        response = self.client.post(
            self.like_comment_url,
            content_type='application/json'
        )
        response = self.client.delete(
            self.like_comment_url,
            content_type='application/json'
        )
        self.assertIn(
            "cannot unlike",
            response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_dislike_nonexistent_comment(self):
        self.add_comment()
        response = self.client.post(
            reverse(
                'comments:comment-dislike',
                kwargs={'pk': self.comment_id + 1}),
            content_type='application/json'
        )
        self.assertIn(
            "not found",
            response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_dislike_comment_you_did_not_author(self):
        self.add_comment()
        self.authenticate_test_user()
        response = self.client.post(
            self.dislike_comment_url,
            content_type='application/json'
        )
        self.assertIn(
            "success",
            response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_get_dislike_status_of_comment(self):
        self.add_comment()
        response = self.client.get(
            self.dislike_comment_url,
            content_type='application/json'
        )
        self.assertIn(
            "success",
            response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_dislike_comment_more_than_once(self):
        self.add_comment()
        self.authenticate_test_user2()
        response = self.client.post(
            self.dislike_comment_url,
            content_type='application/json'
        )
        response = self.client.post(
            self.dislike_comment_url,
            content_type='application/json'
        )
        self.assertIn(
            "can only dislike once",
            response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
