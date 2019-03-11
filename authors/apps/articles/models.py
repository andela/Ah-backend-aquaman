from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
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
    user_rating = models.CharField(max_length=10, default='0')

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['id']

    def __str__(self):
        return f"{self.title}"

    @property
    def average_rating(self):
        """
        method to calculate the average rating of the article.
        """
        ratings = self.ratings.all().aggregate(score=models.Avg("score"))
        return float('%.2f' % (ratings["score"] if ratings['score'] else 0))


class ArticleLikesDislikes(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    likes = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


class Rating(models.Model):
    """
    Model for rating an article
    """
    article = models.ForeignKey(
        Article, related_name="ratings", on_delete=models.CASCADE)
    rated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="scores", null=True)
    rated_on = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["-score"]
