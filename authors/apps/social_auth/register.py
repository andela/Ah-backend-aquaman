from django.contrib.auth import authenticate
from authors.apps.authentication.models import User
from authors.apps.authentication.renderers import UserJSONRenderer


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email:
        registered_user = authenticate(email=email, password="XXXXXXXX")
        return {
            'username': registered_user.username,
            'email': registered_user.email,
            'token': registered_user.token}

    else:
        user = {
            'username': name, 'email': email, 'password': 'XXXXXXXX'}
        User.objects.create_user(**user)
        new_user = authenticate(email=email, password="XXXXXXXX")
        return new_user.token
