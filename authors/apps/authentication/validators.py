import re

from django.shortcuts import get_object_or_404

from rest_framework import serializers

from authors.apps.authentication.models import User

def validate_email(email):
    check_email = User.objects.filter(email=email)
    if not re.search(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', email):
        raise serializers.ValidationError("Incorrect email format please try again")
    if check_email.exists():
        raise serializers.ValidationError("This email has already been used to create a user")
    return email
