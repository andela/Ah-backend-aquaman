"""
Test comments app
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

    def test_create_a_comment(self):
        """
        Test commenting on an article 
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        response = self.client.post(url, data=comment, format="json")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(comment["comment"]["body"], data["comment"]["body"])

    def test_get_single_comment(self):
        """
        Test retriving a single comment
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={"slug":slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:single_comment", kwargs={"slug":slug, "pk":comment_id})
        response = self.client.get(fetch_url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(str(comment_id), str(data["comment"]["id"]))

    def test_update_a_comment(self):
        """
        Test updating a comment 
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={"slug":slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:single_comment", kwargs={"slug":slug, "pk":comment_id})
        response = self.client.put(fetch_url, data=update_comment, format="json")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(update_comment["comment"]["body"], data["body"])

    def test_update_a_comment_same_data(self):
        """
        Test update comment with the same data 
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={"slug":slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:single_comment", kwargs={"slug":slug, "pk":comment_id})
        response = self.client.put(fetch_url, data=comment, format="json")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Please ensure the comment body has changed",
                data["message"])

    def test_update_a_comment_not_yours(self):
        """
        Test update a comment you did not create 
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={"slug":slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:single_comment", kwargs={"slug":slug, "pk":comment_id})
        self.user_access2()
        response = self.client.put(fetch_url, data=update_comment, format="json")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("You can only edit a comment you created",
                data["message"])

    def test_get_all_comments(self):
        """
            test to get all comments

        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={"slug":slug})
        self.client.post(url, data=comment, format="json")
        response = self.client.get(url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(comment["comment"]["body"], data["comments"][0]["body"])

    def test_delete_comment(self):
        """
            tests to delete a comment
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={"slug":slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:single_comment", kwargs={"slug":slug, "pk":comment_id})
        response = self.client.delete(fetch_url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Comment successfully deleted",
                data["message"])

    def test_delete_comment_not_yours(self):
        """
        Test delete a comment you did not create 
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={"slug":slug})
        res = self.client.post(url, data=comment, format="json")
        data = res.data
        comment_id = data["comment"]["id"]
        fetch_url = reverse("comments:single_comment", kwargs={"slug":slug, "pk":comment_id})
        self.user_access2()
        response = self.client.delete(fetch_url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("You can only delete a comment you created",
                data["message"])
