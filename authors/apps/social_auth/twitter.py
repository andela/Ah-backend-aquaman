import twitter


class TwitterAuthTokenVerification:
    """
    class to decode user access_token and user access_token_secret
    tokens will combine the user access_token and access_token_secret
    separated by space
    """
    @staticmethod
    def extract_twitter_auth_tokens(tokens):
        """
        extract_twitter_auth_tokens methods returns user access token and
        its secret required to validate a user
        """
        auth_tokens = tokens.split(' ')
        if len(auth_tokens) != 2:
            return 'invalid token', 'invalid token'
        user_access_token_key = auth_tokens[0]
        user_access_token_secret = auth_tokens[1]
        return user_access_token_key, user_access_token_secret

    @staticmethod
    def validate_twitter_auth_tokens(tokens):
        """
        validate_twiiter_auth_tokens methods returns a twitter
        user profile info
        """
        access_token_key, access_token_secret =\
            TwitterAuthTokenVerification.extract_twitter_auth_tokens(tokens)
        try:
            consumer_api_key = 'KKOhCFzKY3UVMrnG9rK94cEQk'
            consumer_api_secret_key = \
                'WG6sXuSwmu7YU2JjMZxEJ2JqgXuZxRRS8hbtgyF8n1Px6l8aDI'

            api = twitter.Api(
                consumer_key=consumer_api_key,
                consumer_secret=consumer_api_secret_key,
                access_token_key=access_token_key,
                access_token_secret=access_token_secret
            )

            user_profile_info = api.VerifyCredentials(include_email=True)
            return user_profile_info.__dict__

        except:
            return None
