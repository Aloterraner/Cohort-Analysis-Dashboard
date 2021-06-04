"""bootstrapdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from blog_app import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from bootstrapdjango import settings

urlpatterns = [
    path("", views.home, name="home"),
    url(r"^logmanagement/", include("log_management.urls")),
    # url(r'^rolemining/', include(role_mining.urls))
    path("filter", include("log_filtering.urls")),
    path("group_analysis", include("group_analysis.urls")),
    path("views", include("perspective_views.urls")),
    url(r"^groupmanagement/", include("group_management_views.urls")),
]
urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
