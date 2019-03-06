import json

from rest_framework import renderers


class ArticleJSONRenderer(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        # Method is responsible for displaying an article
        return json.dumps({"article": data})
