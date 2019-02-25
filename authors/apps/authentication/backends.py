from rest_framework import authentication

"""Configure JWT Here"""

class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        pass