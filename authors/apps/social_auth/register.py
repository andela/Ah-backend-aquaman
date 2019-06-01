from django.contrib.auth import authenticate
from authors.apps.authentication.models import User
from authors.apps.authentication.renderers import UserJSONRenderer


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email:
        registered_user = authenticate(email=email, password="XXXXXXXX")
        try:
            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'token': registered_user.token}
        except TypeError as identifier:
            return {
                   "message": "something went wrong"
               }
        finally:
            return {
                "message":"something went wrong"
            }


    else:
        user = {
            'username': name, 'email': email, 'password': 'XXXXXXXX'}
        User.objects.create_user(**user)

        user = User.objects.filter(email=email).first()
        user.is_verified = True
        user.save()

        new_user = authenticate(email=email, password="XXXXXXXX")
        return {
            'username': new_user.username,
            'email': new_user.email,
            'token': new_user.token}
