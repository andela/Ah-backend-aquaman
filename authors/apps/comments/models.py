from django.db import models
from authors.apps.articles.models import Article
from authors.apps.profiles.models import Profile


class Comment(models.Model):
    commented_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, to_field='slug')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.body)
