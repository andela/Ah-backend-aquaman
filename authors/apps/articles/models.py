from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from authors.apps.profiles.models import Profile
from django.contrib.postgres.fields import ArrayField

from authors.settings import WORD_LENGTH, WORD_PER_MINUTE


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
    tagList = ArrayField(models.CharField(
        max_length=200), default=list, blank=True)

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

    @staticmethod
    def get_all_tags():
        """Gets all tags on all articles """
        tags = Article.objects.values('tagList').distinct()
        tag_list = []
        for t in tags:
            for tt in t.values():
                tag_list.append(tt)
        return tag_list

    @property
    def read_time(self):
        """This method calculates the read time of an article"""
        word_count = 0
        word_count += len(self.body) / WORD_LENGTH
        result = int(word_count / WORD_PER_MINUTE)
        if result >= 1:
            read_time = str(result) + " minute read"
        else:
            read_time = " less than a minute read"
        return read_time


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
