"""channelworm URL Configuration

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
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('account.urls', namespace='account')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^digitizer/', include('digitizer.urls', namespace="digitizer"), ),
    url(r'^ion_channel/', include('ion_channel.urls', namespace="ion_channel"), ),
    url(r'^index$', 'ion_channel.views.index' ),
    url(r'^$', 'ion_channel.views.index' ,name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

