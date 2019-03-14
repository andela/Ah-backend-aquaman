from django.db import models
from authors.apps.profiles.models import Profile


class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    image = models.URLField(blank=True)
    readtime = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['id']

    def __str__(self):
        return f"{self.title}"


class ArticleLikesDislikes(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    likes = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
