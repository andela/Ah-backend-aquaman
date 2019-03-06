from rest_framework.test import APITestCase
from rest_framework import status


class SocialTests(APITestCase):

    def setUp(self):

        self.user_with_valid_facebook_token = {
            "user": {
                "auth_token": 'EAAIYGXurtOABAD9f7ZB954eYv1FgvfN3EJ\
                    GYuElkvDsj20SrXYTHwigAJP2lirZC4A57ZBL2ZAIPNHknup\
                        oFyf84xliO1U2pvlp0nb3z9tSluZCrviByN8DWKDpcYeEm\
                        2WqJG6ICCawX4m9jiQuVP0J012ZBXZCpAoZD'
            }
        }

        self.user_with_invalid_token = {
            "user": {
                "auth_token": 'EAAIYGXurtOABALi5e5YRlG0Cv7p7SYZAPeC3p9gSB\
                    ItLPP8i'
            }
        }

        self.user_with_valid_twitter_tokens = {
            "user": {
                "auth_token":
                "532504148-qllWlX5cm1bGylVMnJr023wzOmzHVIl1gCjJj6wy J3oNyC3y3ZlUlV4FeXGo3Kadgc9OSMVcM2YoWF9PiS8Jn"
            }
        }

    def test_login_with_invalid_google_token(self):
        """
        Test login with an invalid or expired google token
        """
        response = self.client.post(
            "/api/social/auth/google/", self.user_with_invalid_token,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'The token is invalid or expired. Please login again.',
            str(response.data))

    def test_login_with_invalid_facebook_token(self):
        """
        Test if a user can login with an invalid or expired facebook token
        """
        response = self.client.post(
            "/api/social/auth/facebook/", self.user_with_invalid_token,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'The token is invalid or expired. Please login again.',
            str(response.data))

    def test_login_with_valid_facebook_token(self):
        """
        Test if a user can login with an invalid or expired facebook token
        """
        response = self.client.post(
            "/api/social/auth/facebook/", self.user_with_valid_facebook_token,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_twitter_token(self):
        """
        Test if a user can login with an invalid or expired twitter token
        """
        response = self.client.post(
            "/api/social/auth/twitter/", self.user_with_invalid_token,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'The token is invalid or expired. Please login again.',
            str(response.data))

    def test_login_with_valid_twitter_token(self):
        """
        Test if a user can login with an valid twitter token
        """
        response = self.client.post(
            "/api/social/auth/twitter/", self.user_with_valid_twitter_tokens,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_existing_twitter_user(self):
        """
        Test if a user can login if they already have an account
        """
        response = self.client.post(
            "/api/social/auth/twitter/", self.user_with_valid_twitter_tokens,
            format='json')
        self.client.post(
            "/api/social/auth/twitter/", self.user_with_valid_twitter_tokens,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
