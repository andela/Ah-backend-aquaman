from .models import Article
from django.template.defaultfilters import slugify


class Utils:
    @staticmethod
    def create_slug(article):
        """creates a slug from title,appends an id value for uniqueness"""
        try:

            last = Article.objects.latest().id

            slug = slugify(str(last)+"-"+article)

            return slug
        except Article.DoesNotExist as err:
            return slugify(article)
