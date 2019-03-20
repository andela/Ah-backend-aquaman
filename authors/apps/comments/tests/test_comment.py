"""
Test comments app
"""
from django.urls import reverse
from rest_framework import status

from ..tests.test_data import (
    post_article,
    comment,
    update_comment,
    comment_correct_ranges,
    comment_out_of_index,
    comment_greater_value,
    comment_not_interger_value
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
        self.assertIn(comment["body"], data["comment"]["body"])

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
        self.assertIn(update_comment["body"], data["body"])

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
        self.assertIn(comment["body"], data["comments"][0]["body"])

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

    def test_successfull_highlight_text(self):
        """
        Test if user can hightlight and comment on text successfully.
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        response = self.client.post(url, data=comment_correct_ranges, format="json")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["comment"]["highlighted_text"], "One of")

    def test_values_out_of_index(self):
        """
        Test if user has values which are out of index.
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        response = self.client.post(url, data=comment_out_of_index, format="json")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["error"], "first_highlited or last_highlited is out of index.")

    def test_first_value_greater_than_last(self):
        """
        Test if user has used a first value  which greater than last one.
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        response = self.client.post(url, data=comment_greater_value, format="json")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["error"], "first_highlited should be less than last_highlited.")

    def test_wrong_integer_value(self):
        """
        Test if user used integer values for first or last value.
        """
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        response = self.client.post(url, data=comment_not_interger_value, format="json")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["error"], "first_highlited and last_highlited fields should be intergers.")
