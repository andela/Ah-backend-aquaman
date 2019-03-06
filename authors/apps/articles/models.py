from django.db import models
from authors.apps.profiles.models import Profile


class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    image = models.URLField(blank=True)

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['id']

    def __str__(self):
        return f"{self.title}"
