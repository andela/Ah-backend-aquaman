from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from rest_framework.response import Response
from rest_framework import status
from authors.apps.profiles.models import Profile
from django.contrib.postgres.fields import ArrayField

from authors.settings import WORD_LENGTH, WORD_PER_MINUTE


class ArticleManager(models.Manager):
    """
    In our article manager we are going to specify
    methods relating to how to handle favoriting an article
    """
    def handle_favorite_an_article(self, user_obj, slug):
        
        user_profile = Profile.objects.filter(user=user_obj).first()
        article_to_favorite = self.model.objects.filter(slug=slug).first()
        article_to_favorite.favoritesCount = article_to_favorite.favorites.count() + 1
        article_to_favorite.favorited = True
        article_to_favorite.favorites.add(user_profile)
        article_to_favorite.save()
        return Response({
            "message": "Article has been added to favorites"
        },status=status.HTTP_201_CREATED)

    def unfavorite_an_article(self, request_user, slug):
        article_slug = slug
        user_obj = request_user
        user_ = Profile.objects.get(user=user_obj)
        unfavorite_article = self.model.objects.get(slug=article_slug)
        if unfavorite_article.favorites.count():
            unfavorite_article.favoritesCount = unfavorite_article.favorites.count() - 1
            unfavorite_article.favorites.remove(user_)
            unfavorite_article.favorited =  unfavorite_article.favorites.count() > 0
            unfavorite_article.save()
            return Response({
            "message": "Article has been removed from favorites"
        },status=status.HTTP_200_OK)

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="author_articles"
    )
    body = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    image = models.URLField(blank=True)
    user_rating = models.CharField(max_length=10, default='0')
    tagList = ArrayField(
        models.CharField(max_length=200),
        default=list,
        blank=True,
    )
    favorites = models.ManyToManyField(Profile, related_name='favorited_articles', blank=True)
    favorited = models.BooleanField(default=False)
    favoritesCount = models.IntegerField(default=0)
    objects = ArticleManager()
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
