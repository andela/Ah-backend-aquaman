from django.db import models
from authors.apps.articles.models import Article
from authors.apps.profiles.models import Profile


class Comment(models.Model):
    commented_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        to_field='slug'
    )
    body = models.TextField()
    first_highlited = models.PositiveIntegerField(null=True, blank=True)
    last_highlited = models.PositiveIntegerField(null=True, blank=True)
    highlighted_text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.body)
