"""
Test Liking a comment
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

    def test_like_a_comment(self):
        """
        Test liking a comment 
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:comment-like", kwargs={"slug":slug, "pk":comment_id})
        response = self.client.put(fetch_url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("comment liked successfully", data["message"])

    def test_like_a_comment_twice(self):
        """
        Test liking a comment twice
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:comment-like", kwargs={"slug":slug, "pk":comment_id})
        self.client.put(fetch_url)
        response = self.client.put(fetch_url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("you already liked this comment", data["message"])

    def test_getting_likes_on_a_comment(self):
        """
        Test getting likes on a comment 
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:comment-like", kwargs={"slug":slug, "pk":comment_id})
        self.client.put(fetch_url)
        response = self.client.get(fetch_url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("1", str(data["likesCount"]))

    def test_unlike_comment(self):
        """
            tests to unlike a comment
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:comment-like", kwargs={"slug":slug, "pk":comment_id})
        self.client.put(fetch_url)
        response = self.client.delete(fetch_url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("unliked comment successfully", data["message"])

    def test_unlike_comment_not_liked(self):
        """
        Test unlike a comment you had not liked 
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:comment-like", kwargs={"slug":slug, "pk":comment_id})
        response = self.client.delete(fetch_url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("you have not yet liked this comment", data["message"])
