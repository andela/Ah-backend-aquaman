from django.urls import reverse
from rest_framework import status
from ...comments.tests.base import BaseTestCase
from ...comments.tests.test_data import (
    post_article,
    comment
)
from ...authentication.tests.test_base import BaseTest
from ...articles.tests.base_class import ArticlesBaseTest
from ...articles.models import Article
from ..utils import NotificationSettingsRenderer


class TestNotification(BaseTestCase, ArticlesBaseTest, BaseTest):

    def test_view_all_notifications(self):
        """Tests if user can view all notifications."""
        self.add_other_article()
        article = Article.objects.filter(author__user__username="crycetruly").first()
        self.client.post(reverse("articles:article-favorite", kwargs={'slug': article.slug}))
        url = reverse("comments:post_comment", kwargs={'slug': article.slug})
        self.client.post(url, data=comment, format="json")

        response = self.client.get(reverse("notifications:viewnotifications"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notifications'][0]['title'], 'Article comments')

    def test_view_unread_notifications(self):
        """Tests if user can view unread notifications."""
        self.add_other_article()
        article = Article.objects.filter(author__user__username="crycetruly").first()
        self.client.post(reverse("articles:article-favorite", kwargs={'slug': article.slug}))
        url = reverse("comments:post_comment", kwargs={'slug': article.slug})
        self.client.post(url, data=comment, format="json")

        response = self.client.get(reverse("notifications:unreadnotifications"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notifications'][0]['status'], False)

    def test_user_change_settings(self):
        """Tests if user can change settings."""
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        self.client.post(url, data=comment, format="json")

        response = self.client.put(
            reverse("notifications:optoutnotifications", kwargs={'type': 'email'}),
            data={"settings": False}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_wrong_settings(self):
        """Tests if user used wrong settings"""
        self.user_access()
        self.posting_article(post_article)
        slug = self.article_slug()
        url = reverse("comments:post_comment", kwargs={'slug': slug})
        self.client.post(url, data=comment, format="json")

        response = self.client.put(
            reverse("notifications:optoutnotifications", kwargs={'type': 'notif'}),
            data={"settings": False}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_single_notifications(self):
        """Tests if user can view single notification."""
        self.add_other_article()
        article = Article.objects.filter(author__user__username="crycetruly").first()
        self.client.post(reverse("articles:article-favorite", kwargs={'slug': article.slug}))
        url = reverse("comments:post_comment", kwargs={'slug': article.slug})
        self.client.post(url, data=comment, format="json")

        resp = self.client.get(reverse("notifications:viewnotifications"))
        single = resp.data['notifications'][0]

        response = self.client.get(
            reverse("notifications:singlenotification", kwargs={'slug': single['slug']})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notification'][0]['title'], "Article comments")

    def test_wrong_single_notifications(self):
        """Tests if user used a wrong notification that doesnot exist."""
        self.add_other_article()
        article = Article.objects.filter(author__user__username="crycetruly").first()
        self.client.post(reverse("articles:article-favorite", kwargs={'slug': article.slug}))
        url = reverse("comments:post_comment", kwargs={'slug': article.slug})
        self.client.post(url, data=comment, format="json")

        response = self.client.get(
            reverse("notifications:singlenotification", kwargs={'slug': "wrong-slug"})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "notification not found.")

    def test_notification_settings(self):
        """Tests a user settings function in utilities."""
        self.register_and_login_user()
        response = NotificationSettingsRenderer.render_notification_settings("Bagzie12")
        self.assertEqual(response.data['message'], "notification settings created successfully")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
