"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls

schema_view = get_schema_view(
    openapi.Info(
        title="AQUAMAN AUTHOR'S HAVEN API",
        default_version='v1',
        description="A place where different authors pen down their thoughts",
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(('authors.apps.authentication.urls',
                          'authentication'), namespace='authentication')),

    path('api/', include(('authors.apps.profiles.urls',
                          'profiles'), namespace='profiles')),

    path('api/', include(('authors.apps.articles.urls',
                      'articles'), namespace='articles')),
    path('api/', include(('authors.apps.comments.urls',
                      'comments'), namespace='comments')),

    path('apidocs/', schema_view.with_ui('swagger',
                                         cache_timeout=0),
         name='schema-swagger-ui'),
    path('', include_docs_urls(
        title="AQUAMAN AUTHOR'S HAVEN API",
        description="A place where different authors pen down their thoughts")),
    path('api/social/', include('authors.apps.social_auth.urls')),
]
