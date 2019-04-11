"""
Test retrive edit history of
a comment
"""
from django.urls import reverse
from rest_framework import status

from ..tests.test_data import (post_article, comment,
                                update_comment
                    )

from authors.apps.comments.tests.base import BaseTestCase


class TestComment(BaseTestCase):
    """
    test class to contain functions to handle test for the commenting on an article
    """

    def test_get_history_no_update(self):
        """
        Test get comment history without
        updating the comment 
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:comment_history", kwargs={'pk':comment_id})
        response = self.client.get(fetch_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(comment["body"], 
                response.data["history"][0]["comment_body"])

    def test_get_history_update(self):
        """
        Test get comment history
        after updating comment
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={"slug":slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        update_url = reverse("comments:single_comment", kwargs={"slug":slug, "pk":comment_id})
        self.client.put(update_url, data=update_comment, format="json")
        fetch_url = reverse("comments:comment_history", kwargs={'pk':comment_id})
        response = self.client.get(fetch_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(update_comment["body"],
                    response.data["history"][0]["comment_body"])

    def test_get_history_wrong_user(self):
        """
        Test user trying to access 
        another users comment history
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:comment_history", kwargs={'pk':comment_id})
        self.user_access2()
        response = self.client.get(fetch_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("You didn't create this comment Access Denied", 
                response.data["message"])

    def test_get_history_wrong_comment_id(self):
        """
        Test user enter wrong comment id
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        self.client.post(url, data=comment, format="json")
        fetch_url = reverse("comments:comment_history", kwargs={'pk':4})
        response = self.client.get(fetch_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Not found", response.data["detail"])
