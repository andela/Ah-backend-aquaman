from django.db import models
from authors.apps.articles.models import Article
from authors.apps.profiles.models import Profile
from simple_history.models import HistoricalRecords


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
    comment_history = HistoricalRecords()

    def __str__(self):
        return str(self.body)

class CommentLike(models.Model):
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE)
    like_status=models.BooleanField()
    liked_by=models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.liked_by)
